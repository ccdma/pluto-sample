from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, time, csv
from adiutil.device import Device
from adiutil.static import *
from itertools import zip_longest
from flow import DeviceFlow, TxFlow
from pica.ica import const_powerd_samples, primitive_root_code, weyl_samples

np.random.seed(1)

class NormalTxFlow(TxFlow):

	def __init__(self, device: Device, samplings: np.ndarray) -> None:
		super().__init__()
		self.samplings = samplings
		self.device = device
		self.sdr = device.get_pluto()
		self.save_file()

	def on_init(self):
		sdr = self.sdr
		sdr.tx_lo = DEFAULT_TX_LO
		sdr.tx_rf_bandwidth = DEFAULT_TX_BW
		sdr.sample_rate = SAMPLE_RATE
		sdr.tx_cyclic_buffer = True
		self.sdr.tx_destroy_buffer()
	
	def on_send_start(self):
		print(f"{self.sdr.uri} started")
		self.sdr.tx(self.samplings*1024)
	
	def on_send_end(self):
		self.sdr.tx_destroy_buffer()
	
	def on_destroy(self):
		self.sdr.tx_destroy_buffer()
	
	def save_file(self):
		basedir = Path("out/send")
		basedir.mkdir(parents=True, exist_ok=True)
		with open(basedir/f"send-{self.device.serial[-5:]}.csv", "w+") as f:
			c = csv.writer(f)
			c.writerow(self.samplings.real)
			c.writerow(self.samplings.imag)


# np.array()で信号を生成すること！（途中の演算はnp.arrayをを想定している）
if __name__ == "__main__":
	SAMPLINGS = 1024
	DEVICES = adiutil.DeviceList()

	flows = [
		NormalTxFlow(DEVICES.find("d87"), const_powerd_samples(2, np.pi/(1+np.sqrt(2)), SAMPLINGS)*4),
		NormalTxFlow(DEVICES.find("9ce"), const_powerd_samples(2, np.pi/(1+np.sqrt(3)), SAMPLINGS)*4)
	]

	try:
		for flow in flows:
			flow.on_init()

		print("init sleep started")
		time.sleep(3.0)
		print("init sleep end")

		flows[0].on_send_start()
		time.sleep(0.01)
		flows[1].on_send_start()

		time.sleep(TIME)
		
		for flow in flows:
			flow.on_send_end()
		
		for flow in flows:
			flow.on_before_destroy()

	finally:
		for flow in flows:
			flow.on_destroy()

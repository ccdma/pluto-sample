import numpy as np
import matplotlib.pyplot as plt
from numpy.random.mtrand import sample
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy, pylab, time
import adiutil, csv
from adiutil.device import Device
from adiutil.static import *
from pathlib import Path

from flow import RxFlow

class NormalRxFlow(RxFlow):

	def __init__(self, device: Device) -> None:
		super().__init__()
		self.device = device
		self.sdr = device.get_pluto()
		self.samplings = None

	def on_init(self):
		sdr = self.sdr
		sdr.rx_lo = DEFAULT_RX_LO
		sdr.rx_rf_bandwidth = DEFAULT_RX_BW
		sdr.sample_rate = SAMPLE_RATE
		sdr.rx_buffer_size = int(1*MHz)
		self.destroy_buffer()

	def on_read_start(self):
		self.destroy_buffer()
		print(f"{self.sdr.uri} read")

	def on_read_end(self):
		self.samplings = self.sdr.rx()
		
	def on_before_destroy(self):
		basedir = Path("out/receive")
		basedir.mkdir(parents=True, exist_ok=True)
		samplings = np.array(self.samplings)
		with open(basedir/f"receive-{self.device.serial[-5:]}.csv", "w+") as f:
			c = csv.writer(f)
			c.writerow(samplings.real)
			c.writerow(samplings.imag)
	
	def on_destroy(self):
		self.destroy_buffer()

	def destroy_buffer(self):
		self.sdr.tx_destroy_buffer()
		self.sdr.rx_destroy_buffer()

if __name__ == "__main__":
	DEVICES = adiutil.DeviceList()

	flows = [
		NormalRxFlow(DEVICES.find("3a0")),
		NormalRxFlow(DEVICES.find("f24")),
	]

	try:
		for flow in flows:
			flow.on_init()

		print("init sleep started")
		time.sleep(1.0)
		print("init sleep end")

		for flow in flows:
			flow.on_read_start()

		time.sleep(1.0)

		for flow in flows:
			flow.on_read_end()

		for flow in flows:
			flow.on_before_destroy()

	finally:
		for flow in flows:
			flow.on_destroy()

from pathlib import Path
from typing import List
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
from save_multi import NormalRxFlow
from send_multi import NormalTxFlow
import threading

if __name__ == "__main__":
	SAMPLINGS = 1024
	DEVICES = adiutil.DeviceList()

	tx_flows = [
		NormalTxFlow(DEVICES.find("d87"), const_powerd_samples(2, np.pi/(1+np.sqrt(2)), SAMPLINGS)*4),
		NormalTxFlow(DEVICES.find("9ce"), const_powerd_samples(2, np.pi/(1+np.sqrt(3)), SAMPLINGS)*4)
	]

	rx_flows = [
		NormalRxFlow(DEVICES.find("3a0")),
		NormalRxFlow(DEVICES.find("f24")),
	]

	flows: List[DeviceFlow] = tx_flows + rx_flows

	try:
		for flow in flows:
			flow.on_init()

		print("init sleep started")
		time.sleep(3.0)
		print("init sleep end")

		tx_flows[0].on_send_start()
		time.sleep(1.0)

		def target():
			time.sleep(0.01)
			tx_flows[1].on_send_start()
		tf1 = threading.Thread(target=target)
		tf1.start()

		rx_read_threads = []
		for flow in rx_flows:
			def target():
				f = flow
				f.on_read()
			t = threading.Thread(target=target)
			t.start()
			rx_read_threads.append(t)

		tf1.join()
		for thread in rx_read_threads:
			t.join()
		
		print(f"end reading ({time.time()})")
		for flow in tx_flows:
			flow.on_send_end()
		for flow in flows:
			flow.on_before_destroy()

	finally:
		for flow in flows:
			flow.on_destroy()

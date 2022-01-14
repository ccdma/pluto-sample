from pathlib import Path
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, time, csv, sys
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

	prefix = None
	if len(sys.argv) > 1:
		prefix = sys.argv[1]

	tx_flow = NormalTxFlow(DEVICES.find("d87"), const_powerd_samples(2, np.pi/(1+np.sqrt(2)), SAMPLINGS)*4)
	rx_flow = NormalRxFlow(DEVICES.find("3a0"), buffer_size=100*KHz, filename_prefix=prefix)

	try:
		tx_flow.on_init()
		rx_flow.on_init()

		print("init sleep started")
		time.sleep(1.0)
		print("init sleep end")

		tx_flow.on_send_start()
		time.sleep(1.0)
		rx_flow.on_read()
		
		tx_flow.on_send_end()

		rx_flow.on_before_destroy()		
		tx_flow.on_before_destroy()

	finally:
		rx_flow.on_destroy()
		tx_flow.on_destroy()

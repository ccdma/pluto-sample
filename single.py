import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, time
from adiutil.static import *
from pica.ica import const_powerd_samples

np.random.seed(1)

DEVICES = adiutil.DeviceList()

if __name__ == "__main__":
	# com = np.array([np.exp(2j*np.pi*i*4/1024) for i in range(1024)])
	com = const_powerd_samples(2, np.pi/(1+np.sqrt(2)), 1024)
	# print(com[:10])
	upsampled = com*2**3

	sdr = DEVICES.find("1044734c9605000d15003300deb64fb9ce").get_pluto()
	# sdr.tx_hardwaregain = 0
	
	start = time.time()
	print(f"{sdr.uri} started")
	sdr.tx_cyclic_buffer = True
	idx = 0
	sdr.tx(upsampled[idx:idx+1023]*1024)
	time.sleep(TIME)
	sdr.tx_destroy_buffer() # バッファを消してやらないとセグフォ？

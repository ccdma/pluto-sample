import numpy as np
import matplotlib.pyplot as plt
from numpy.random.mtrand import sample
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy, pylab, time
import adiutil, csv
from adiutil.static import *

DEVICES = adiutil.DeviceList()

if __name__ == "__main__":
	sdr = DEVICES.find("1044734c96050013f7ff27004a464f13a0").get_pluto()
	sdr.rx_lo = DEFAULT_RX_LO
	sdr.rx_rf_bandwidth = DEFAULT_RX_BW
	sdr.sample_rate = SAMPLE_RATE
	sdr.rx_buffer_size = 1024*2**2
	time.sleep(1)

	samples = []
	start = time.time()
	# while (time.time() - start) < TIME-5.0:
	samples.extend(sdr.rx())
	samples = np.array(samples)#[center:center+10000]

	with open("out/receive.csv", "w+") as f:
		writer = csv.writer(f)
		writer.writerow(samples.real.tolist())
		writer.writerow(samples.imag.tolist())

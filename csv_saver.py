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

	samples = []
	start = time.time()
	while (time.time() - start) < TIME-5.0:
		samples.extend(sdr.rx())
	center = len(samples)-5000
	samples = np.array(samples)[center:center+10000]

	with open("out/result.csv", "w+") as f:
		writer = csv.writer(f)
		writer.writerow(samples.real.tolist())
		writer.writerow(samples.imag.tolist())

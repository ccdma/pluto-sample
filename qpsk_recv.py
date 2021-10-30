import numpy as np
import matplotlib.pyplot as plt
from numpy.random.mtrand import sample
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy, pylab, time
import adiutil
from adiutil.static import *

DEVICES = adiutil.DeviceList()

if __name__ == "__main__":
    sdr = DEVICES.find("1044734c96050013f7ff27004a464f13a0").get_pluto()
    sdr.sample_rate = int(2.4e6)

    samples = []
    start = time.time()
    while (time.time() - start) < TIME-3.0:
        samples.extend(sdr.rx())
    samples = np.array(samples)[:4000]

    # QPSKコンスタレーション
    plt.figure()
    plt.plot(samples.real, samples.imag, lw=1)
    plt.scatter(samples.real, samples.imag, s=2)
    plt.show()

    # yf = fft.fft(samples)
    # yf = fft.fftshift(yf)
    # N = int(len(yf))
    # targetrate = 9600*150
    # xf = np.linspace(-targetrate/2.0, targetrate/2.0, N)
    # plt.figure()
    # plt.semilogy(xf, np.abs(yf[:N]), '-b')
    plt.show()

    # pylab.psd(samples, NFFT=1024, Fs=sdr.sample_rate/MHz, Fc=sdr.sample_rate/MHz)

    # pylab.xlabel("Frequency (MHz)")
    # pylab.ylabel("relative power (db)")
    # pylab.show()
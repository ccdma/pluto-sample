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
    sdr.rx_lo = DEFAULT_RX_LO
    sdr.rx_rf_bandwidth = DEFAULT_RX_BW
    sdr.sample_rate = SAMPLE_RATE

    samples = []
    start = time.time()
    while (time.time() - start) < TIME-3.0:
        samples.extend(sdr.rx())
    BEI = 5000
    LEN = 2000
    samples = np.array(samples)[BEI:BEI+LEN]

    # samples = samples/np.abs(samples)

    fig = plt.figure(figsize=(5,5))
    # QPSKコンスタレーション
    # plt.plot(samples.real, samples.imag, lw=0.2)
    plt.scatter(samples.real, samples.imag, s=2)
    plt.savefig("out/AAA")

    # fig = plt.figure()
    # # returnmap
    # plt.scatter(samples[0:-1].real, samples[1:].real, s=2)

    # plt.savefig("out/BBB")
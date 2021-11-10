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
    sdr.sample_rate = 9600*150

    samples = []
    start = time.time()
    while (time.time() - start) < TIME-3.0:
        samples.extend(sdr.rx())
    samples = np.array(samples)[10000:12000]

    fig = plt.figure()
    # QPSKコンスタレーション
    # plt.plot(samples.real, samples.imag, lw=1)
    plt.scatter(samples.real, samples.imag, s=2)
    plt.savefig("out/AAA")

    s_samples = []
    for s in samples:
        arg = np.angle(s, deg=False)
        s_samples.append(complex(np.cos(arg), np.sin(arg)))
    s_samples = np.array(s_samples)

    fig = plt.figure()
    # returnmap
    plt.scatter(samples[0:-1].real, samples[1:].real, s=2)

    plt.savefig("out/BBB")
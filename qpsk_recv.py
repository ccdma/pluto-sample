import adiutil
from pylab import *
import matplotlib.pyplot as plt

KHz = 1000
MHz = 1000*1000
DEVICES = adiutil.DeviceList()

if __name__ == "__main__":
    sdr = DEVICES.find("1044734c96050013f7ff27004a464f13a0").create_pluto()
    sdr.sample_rate = int(2.4e6)
    sdr.rx_lo = 920*MHz
    
    samples = sdr.rx()

    # QPSKコンスタレーション
    plt.figure()
    plt.plot(samples.real, samples.imag, lw=1)
    plt.scatter(samples.real, samples.imag, s=10)
    plt.show()


    # psd(samples, NFFT=1024, Fs=sdr.sample_rate/MHz, Fc=sdr.sample_rate/MHz)

    # xlabel("Frequency (MHz)")
    # ylabel("relative power (db)")
    # show()
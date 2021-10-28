import numpy as np
import matplotlib.pyplot as plt
from adiutil import static
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil
import time, csv, threading
from adiutil.static import *
from ica.algorithm import fastica
from ica.eval import seed
from itertools import zip_longest

DEVICES = adiutil.DeviceList()

rate = 96000
upsample_ratio = 150
targetrate = rate*upsample_ratio

TIME = 15.0

if __name__ == "__main__":
    sdr0 = DEVICES.find("1044734c9605000d15003300deb64fb9ce").create_pluto()
    # sdr1 = DEVICES.find("1044734c96050013f7ff27004a464f13a0").create_pluto()
    
    r_sdrs = []
    t_sdrs = [sdr0]
    
    for sdr in r_sdrs+t_sdrs:
        sdr.tx_lo = 920*MHz
        sdr.rx_lo = 920*MHz
        sdr.tx_hardwaregain_chan0 = 0
        sdr.tx_rf_bandwidth = 100*KHz
        sdr.sample_rate = int(targetrate)
        sdr.rx_rf_bandwidth = 100*KHz

    SERIES = len(t_sdrs)

    S = np.array([seed.chebyt_series(i, 0.1+i/10, 1024*1000) for i in range(SERIES)])
    # fs = int(sdr.sample_rate)
    # N = 1024
    # fc = int(3000000 / (fs / N)) * (fs / N)
    # ts = 1 / float(fs)
    # t = np.arange(0, N * ts, ts)
    # i = np.cos(2 * np.pi * t * fc) * 2 ** 14
    # q = np.sin(2 * np.pi * t * fc) * 2 ** 14
    # S = np.array([i + 1j*q for _ in range(SERIES)])

    S_MOD = []
    for s in S:
        resampled = commpy.utilities.upsample(s, upsample_ratio)
        S_MOD.append(s)
    S = np.array(S_MOD)

    rx_bufs = [[] for _ in r_sdrs]

    def send(sdr, s):
        start = time.time()
        while (time.time() - start) < TIME:
            for idx in range(0, len(s), 1024):
                sdr.tx(s[idx:idx+1023]*2**14)
        sdr.tx_destroy_buffer()

    def read(sdr, rx_buf):
        start = time.time()
        while (time.time() - start) < TIME:
            rx_buf.extend(sdr.rx())

    threads = []
    for sdr, s in zip_longest(t_sdrs, S):
        t = threading.Thread(target=send, args=(sdr, s), name=f"{sdr.uri}-send")
        threads.append(t)
    for sdr, rx_buf in zip_longest(r_sdrs, rx_bufs):
        t = threading.Thread(target=read, args=(sdr, rx_buf), name=f"{sdr.uri}-read")
        threads.append(t)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    

    # plt.figure()
    # x = np.array(rx_bufs[0][1024*50:1024*101])
    # f, Pxx_den = sig.periodogram(x, fs)
    # plt.clf()
    # plt.semilogy(f, Pxx_den)
    # plt.ylim([1e-7, 1e2])
    # plt.xlabel("frequency [Hz]")
    # plt.ylabel("PSD [V**2/Hz]")
    # plt.draw()
    # plt.pause(0.05)
    # time.sleep(0.1)

    # plt.figure()
    # yf = fft.fft(rx_bufs[0][1024*50:1024*101])
    # yf = fft.fftshift(yf)
    # N = int(len(yf))
    # xf = np.linspace(-targetrate/2.0, targetrate/2.0, N)
    # plt.semilogy(xf, np.abs(yf[:N]), '-b')

    # plt.figure()
    # b = np.array(rx_bufs[0][1024*100:1024*101])
    # plt.plot(b.real, b.imag, lw=1)
    # plt.scatter(b.real, b.imag, s=10)
    # plt.show()

    # with open('chebyt.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(rx_bufs)


import numpy as np
import matplotlib.pyplot as plt
from adiutil import static
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, adi
import time, csv, threading
from adiutil.static import *
from ica.algorithm import fastica
from ica.eval import seed
from itertools import zip_longest
from typing import List

DEVICES = adiutil.DeviceList()

rate = 96000
upsample_ratio = 150
targetrate = rate*upsample_ratio

if __name__ == "__main__":
    dev0 = DEVICES.find("1044734c9605000d15003300deb64fb9ce")
    dev1 = DEVICES.find("1044734c96050013f7ff27004a464f13a0")
    
    r_devs: List[adiutil.Device] = []
    t_devs: List[adiutil.Device] = [dev0]
    
    for dev in r_devs+t_devs:
        sdr = dev.get_pluto()
        sdr.tx_hardwaregain_chan0 = 0
        sdr.sample_rate = int(targetrate)

    SERIES = len(t_devs)

    S = []
    for i in range(SERIES):
        ser = seed.chebyt_series(i, 0.1+i/10, 1024*1000) 
        S.append(ser + ser*1j)
    S = np.array(S)

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

    rx_bufs = [[] for _ in r_devs]

    def send(dev: adiutil.Device, s):
        sdr = dev.get_pluto()
        start = time.time()
        print(f"{dev.name} started")
        while (time.time() - start) < TIME:
            for idx in range(0, len(s), 1024):
                sdr.tx(s[idx:idx+1023]*2**14)
        sdr.tx_destroy_buffer()

    def read(dev: adiutil.Device, rx_buf):
        sdr = dev.get_pluto()
        start = time.time()
        while (time.time() - start) < TIME:
            rx_buf.extend(sdr.rx())

    threads = []
    for dev, s in zip_longest(t_devs, S):
        t = threading.Thread(target=send, args=(dev, s), name=f"{dev.name}-send")
        threads.append(t)
    for dev, rx_buf in zip_longest(r_devs, rx_bufs):
        t = threading.Thread(target=read, args=(dev, rx_buf), name=f"{dev.name}-read")
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
    # b = np.array(rx_bufs[0][1024*10:1024*11])
    # plt.plot(b.real, b.imag, lw=1)
    # plt.scatter(b.real, b.imag, s=2)
    # plt.show()

    # with open('chebyt.csv', 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(rx_bufs)


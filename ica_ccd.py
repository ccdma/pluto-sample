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

if __name__ == "__main__":
    sdr0 = DEVICES.find("1044734c9605000d15003300deb64fb9ce").create_pluto()
    sdr1 = DEVICES.find("1044734c96050013f7ff27004a464f13a0").create_pluto()
    
    sdrs = [sdr0, sdr1]
    for sdr in sdrs:
        sdr.tx_lo = 920*MHz
        sdr.rx_lo = 920*MHz
        sdr.tx_hardwaregain_chan0 = 0
        sdr.tx_rf_bandwidth = 100*KHz
        sdr.sample_rate = int(targetrate)
        sdr.rx_rf_bandwidth = 100*KHz
    
    r_sdrs = [sdr0]
    t_sdrs = [sdr1]

    SERIES = len(t_sdrs)
    S = np.array([seed.chebyt_series(i, 0.1+i/10, 1024*100) for i in range(SERIES)])

    rx_bufs = [[] for _ in r_sdrs]

    def send(sdr, s):
        start = time.time()
        while (time.time() - start) < 2.0:
            for idx in range(0, len(s), 1024):
                sdr.tx(s[idx:idx+1023]*1024)

    def read(sdr, rx_buf):
        start = time.time()
        while (time.time() - start) < 2.0:
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
    # b = np.array(rx_bufs[0][1024*100:1024*101])
    # plt.plot(b.real, b.imag, lw=1)
    # plt.scatter(b.real, b.imag, s=10)
    # plt.show()

    with open('chebyt.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rx_bufs)


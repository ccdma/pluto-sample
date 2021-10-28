import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, time
from adiutil.static import *

np.random.seed(1)

DEVICES = adiutil.DeviceList()

bits = np.random.randint(0, 2, 1024)
rate = 9600
upsample_ratio = 150
targetrate = rate*upsample_ratio

if __name__ == "__main__":
    # bpsk変調
    bpsk_mod = bits*2 - 1.0
    # qpsk変調
    qpsk_mod = bpsk_mod[::2]+bpsk_mod[1::2]*1.0j
    qpsk_mod = qpsk_mod*(1.0/np.sqrt(2.0))
    # upsample
    upsamp = sig.resample(qpsk_mod, int(len(qpsk_mod)*upsample_ratio))
    h_rrc = commpy.filters.rrcosfilter(len(upsamp), 0.8, 1/rate, targetrate)[1]
    upsampled = np.convolve(h_rrc, upsamp)

    # upsampled = commpy.utilities.upsample(qpsk_mod, upsample_ratio)
    
    # 時系列表示
    # ax1 = plt.subplot(2,1,1)
    # ax2 = plt.subplot(2,1,2)
    # ax1.plot(qpsk_mod.real, drawstyle="steps-post")
    # ax2.plot(qpsk_mod.imag, drawstyle="steps-post")

    # スペクトラム表示（qpsk_mod）
    # yf = fft.fft(upsampled)
    # yf = fft.fftshift(yf)
    # N = int(len(yf))
    # xf = np.linspace(-targetrate/2.0, targetrate/2.0, N)
    # plt.figure()
    # plt.semilogy(xf, np.abs(yf[:N]), '-b')

    # # QPSKコンスタレーション
    # plt.figure()
    # plt.plot(upsampled.real, upsampled.imag, lw=1)
    # plt.scatter(upsampled.real, upsampled.imag, s=10)
    plt.show()

    sdr = DEVICES.find("1044734c9605000d15003300deb64fb9ce").get_pluto()
    sdr.sample_rate = int(targetrate)
    sdr.tx_hardwaregain = 0
    
    start = time.time()
    print(f"{sdr.uri} started")
    while (time.time() - start) < TIME:
        for idx in range(0, len(upsampled), 1024):
            sdr.tx(upsampled[idx:idx+1023]*1024)
    sdr.tx_destroy_buffer() # バッファを消してやらないとセグフォ？

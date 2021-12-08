import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy
import adiutil, time, csv
from adiutil.static import *
from pica.ica import const_powerd_samples, primitive_root_code, weyl_samples

np.random.seed(1)

DEVICES = adiutil.DeviceList()

# np.array()で信号を生成すること！（途中の演算はnp.arrayをを想定している）
if __name__ == "__main__":
    SAMPLINGS = 1024
    # samples = weyl_samples(np.sqrt(0.2), np.sqrt(0.3), SAMPLINGS)
    samples = np.array([np.exp(2j*np.pi*i/SAMPLINGS) for i in range(SAMPLINGS)])
    # samples = primitive_root_code(1019, 2) * 2
    # samples = const_powerd_samples(2, np.pi/(1+np.sqrt(2)), SAMPLINGS) * 2
    samples = np.array(samples) * 2

    sdr = DEVICES.find("9ce").get_pluto()
    sdr.tx_lo = DEFAULT_TX_LO
    sdr.tx_rf_bandwidth = DEFAULT_TX_BW
    sdr.sample_rate = SAMPLE_RATE

    start = time.time()
    print(f"{sdr.uri} started")
    sdr.tx_cyclic_buffer = True
    samples = samples * 1024
    sdr.tx(samples)
    time.sleep(TIME)
    sdr.tx_destroy_buffer() # バッファを消してやらないとセグフォ？


    f = open("out/send.csv", "w+")
    c = csv.writer(f)
    c.writerow(samples.real)
    c.writerow(samples.imag)
    f.close()

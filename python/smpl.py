import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import adi

MHz = 1000*1000

IIO_DEVICES = ["usb:5.2.5"]

sdrs = [*map(lambda uri: adi.Pluto(uri=uri), IIO_DEVICES)]
# sdrs = [adi.Pluto(uri=IIO_DEVICES[0])]
# set parameter
for sdr in sdrs:
    sdr.rx_rf_bandwidth = 4*MHz
    sdr.rx_lo = 920*MHz
    sdr.tx_rf_bandwidth = 4*MHz
    sdr.tx_lo = 920*MHz
    sdr.tx_cyclic_buffer = True
    sdr.tx_hardwaregain_chan0 = -30

sdr0 = sdrs[0]

# Create a sinewave waveform
fs = int(sdr0.sample_rate)
N = 1024
fc = int(3000000 / (fs / N)) * (fs / N)
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q
sdr0.tx(iq)

# Collect data
data = sdr0.rx()

_sin = []
for i,d in enumerate(data):
    _sin.append(d.real*np.cos(2 * np.pi * i * fc) - d.imag*np.sin(2 * np.pi * i * fc))
plt.plot(_sin)

plt.show()

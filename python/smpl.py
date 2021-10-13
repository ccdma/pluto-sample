import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import adi
import subprocess
subprocess.run("ls").stdout
MHz = 1000*1000

# Import library
# Create radio object
sdr = adi.Pluto(uri="usb:3.6.5")
# Configure properties
sdr.rx_rf_bandwidth = 4*MHz
sdr.rx_lo = 920*MHz
sdr.tx_rf_bandwidth = 4*MHz
sdr.tx_lo = 920*MHz
print(sdr)

# Create a sinewave waveform
fs = int(sdr.sample_rate)
N = 1024
fc = int(3000000 / (fs / N)) * (fs / N)
ts = 1 / float(fs)
t = np.arange(0, N * ts, ts)
i = np.cos(2 * np.pi * t * fc) * 2 ** 14
q = np.sin(2 * np.pi * t * fc) * 2 ** 14
iq = i + 1j * q

# Collect data
data = sdr.rx()
data2 = sdr.rx()

# for r in range(20):
#     x = data

#     f, Pxx_den = signal.periodogram(x, fs)
#     plt.clf()
#     plt.semilogy(f, Pxx_den)
#     # plt.ylim([1e-7, 1e2])
#     plt.xlabel("frequency [Hz]")
#     plt.ylabel("PSD [V**2/Hz]")
#     plt.draw()
#     plt.pause(0.05)
#     time.sleep(0.1)

_sin = []
for d in data:
    _sin.append(d.real)
plt.plot(_sin)
plt.plot([*map(lambda c: c.real, data2)])
print(data)

plt.show()

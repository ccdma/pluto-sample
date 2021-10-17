import matplotlib.pyplot as plt
import adi

MHz = 1000*1000

sdr = adi.Pluto()
sdr.rx_rf_bandwidth = 4*MHz
sdr.rx_lo = 920*MHz

data = sdr.rx()

data_r = []
data_i = []
for datum in data:
    data_r.append(datum.real)
    data_i.append(datum.imag)
plt.scatter(data_r, data_i)
plt.xlabel("I")
plt.ylabel("Q")
plt.show()
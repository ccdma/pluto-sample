from pica.ica import const_powerd_samples
import matplotlib.pyplot as plt
import numpy as np

s = const_powerd_samples(3, np.exp(np.pi/12*1j), 1024)

plt.scatter(s.real, s.imag)
plt.show()

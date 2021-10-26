import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
import scipy.fftpack as fft
import commpy, scipy

KHz = 1000
MHz = 1000*1000
DEVICES = adiutil.DeviceList()

rate = 96000
upsample_ratio = 150
targetrate = rate*upsample_ratio


if __name__ == "__main__":
    


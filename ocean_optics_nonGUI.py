# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:18:54 2022
auto-acquiring and save using Oceanoptics maya200pro
@author: shouy
"""
import matplotlib.pyplot as plt
import time
import numpy as np
from seabreeze.spectrometers import Spectrometer
spec = Spectrometer.from_serial_number(serial = 'MAYP111212')
# spec = Spectrometer.from_first_available()
t = spec.integration_time_micros_limits
m = spec.max_intensity
sm = spec.serial_number
model = spec.model
p = spec.pixels
f = spec.features
inten_limit = 500
intime = 20000 #microsecond
if intime < t[0]:
    intime = t[0]
elif intime > t[1]:
    intime = t[1]
alltime = 10 #second
num = alltime*1e6/intime
spec.integration_time_micros(intime)
start_time = time.time()
for i in np.arange(num):
    wavelengths, intensities = spec.spectrum(correct_dark_counts = True)
    if np.max(intensities[10:-5]) > inten_limit:
        print(i)
        break
end_time = time.time()
print(end_time-start_time)
plt.plot(wavelengths,intensities)
spec.close()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 09:43:29 2022

@author: lucas
"""
#%% Check if datapack is installed
import sys

try:
    import vg
except ImportError:
    print ('pycurl is not installed, please type in console "pip install numpy vg"')
    sys.exit()
#%% Libraries
from IPython import get_ipython
get_ipython().magic('reset -sf')

import os, fnmatch
import numpy as np
import matplotlib.pyplot as plt

#%% User specified variables. Change these to fit your own needs.

# Insert the map you want to process here
datafold = '001'

# Insert the amount of measurements per second here
Sample_frequency = 1

#%% Processing of the barometer
matches_bar = []
matches_mag = []

#Calling data and fixing it to 'matches'
for root, dirnames, filenames in os.walk(datafold):
    for filename in fnmatch.filter(filenames,"*Baro.csv"):
        matches_bar.append(os.path.join(root,filename))
    for filename in fnmatch.filter(filenames,"*Mag.csv"):
        matches_mag.append(os.path.join(root,filename))

# Defining the dataset
data_bar = np.loadtxt(matches_bar[0],delimiter=",",skiprows=1) 
Pressure_bar = np.around(data_bar[:,1],2)
Time_bar = data_bar[:,0]

plt.plot(data_bar[:,0],data_bar[:,1],'r')
plt.ylabel('Druk (hPa)')
plt.xlabel('Tijd (s)')
plt.title('Druk ten opzichte van de tijd')
plt.show()
#%% Calculation of time
Begin_pressure = Pressure_bar[0]

#Defining the times
Begintime = np.subtract(Begin_pressure,0.1)
Endtime = np.min(Pressure_bar)

for i in range(len(data_bar)):
    if Pressure_bar[i] == Endtime:
        Endtime_real = Time_bar[i]
    if Pressure_bar[i] == Begintime:
        Begintime_real = Time_bar[i]

# Filters for time
ts_1 = data_bar[:,0] <= Begintime_real
ts_2 = data_bar[:,0] <= Endtime_real

Time_filter = ts_2 & ~ts_1

# Actual function of time
Time = np.int64(np.sum(Time_filter)/Sample_frequency)

print('This climber climbed for',Time,'s')

#%% Calculation of fluidity whilst climbing

# Making array for later use
Fluid_arr = []

# Defining actual time spent climbing
Climb_time = Pressure_bar[Time_filter]

# Deciding if the moment of climbing was fluid
for i in range(len(Climb_time)-1):
    if Climb_time[i] == Climb_time[i+1]:
        fluid = 0
    else:
        fluid = 1
    Fluid_arr.append(fluid)

#Calculating fluidity
Fluidity = np.sum(Fluid_arr)/len(Climb_time)
Fluidity_percent = np.round(Fluidity * 100,1)

print('This climber climbed with a fluidity of',Fluidity_percent,'%')    
#%% Calculation of the eventual number for the climber

# Defines the maxtime
height = np.round((Begin_pressure - Endtime) * 10,2)
print('This climber climbed up to',height,'m high')

maxtime = 300*0.1*height

# Calculating parts of the number
Height_number = height * 0.1
Fluidity_number = Fluidity * 10 * 0.7
Time_number = (1.25 - Time / maxtime) * 10 * 0.2

# Calaculating actual performance mark 
Number = np.round(Height_number + Fluidity_number + Time_number,2)

print('The performance of this climber gets a',Number,'out of ten')

#%% Processing of the magnetometer

# Hier staat de mogelijke extra tijd voorbereiding (inladen)
data_mag = np.loadtxt(matches_mag[0],delimiter=",",skiprows=1) 
time_mag = data_mag[:,0]
x_Versn = data_mag[:,1]
y_Versn = data_mag[:,2]
z_Versn = data_mag[:,3]

# Making empty array for later use
Angle_between = []

# Comparing all angles
for i in range(len(x_Versn)-1):
    vec1 = np.array([x_Versn[i],y_Versn[i],z_Versn[i]])
    vec2 = np.array([x_Versn[i+1],y_Versn[i+1],z_Versn[i+1]])
    Angle = vg.angle(vec1,vec2)
    Angle_between.append(Angle)

# Adding the angle to the defined data of the magnetometer
data_mag = np.c_[data_mag[:len(Angle_between)], Angle_between]

#plotting the final graph
plt.plot(data_mag[:,0],data_mag[:,4],'g')
plt.ylabel('Grootte beweging')
plt.xlabel('Tijd (S)')
plt.title('Grootte beweging ten opzichte van de tijd')
plt.show()

print('Ditmaal geen SO naar JW, maar eig wel want JW is een leipe guy')

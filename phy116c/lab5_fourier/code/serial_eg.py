#
# serial_eg.py
# by Michael Mulhearn
#
# An example program for acquiring data from an Arduino over the serial link and 
# graphically displaying it with SciPy.
#
# 1) Opens a serial connection (you will probably need to adjust this) 
# 2) Waits for Arduino init message.
# 3) Waits for user to press enter to acquire data.
# 4) Sends acquire signal to Arduino
# 5) Retrieves data of the serial link
# 6) Plots the data
#
# *** Requires on Anaconda (SciPy) and PySerial libraries. ***
#

import time, serial
import matplotlib.pyplot as plt
import numpy as np

#SERIAL_PORT="COM4"
SERIAL_PORT="/dev/cu.usbmodem1421"
#SERIAL_PORT=raw_input("Enter the serial port for the Arduino (e.g. COM4):  ")

print "connecting to the Arduino..."

# open the serial connection
ser = serial.Serial(SERIAL_PORT, 115200)
time.sleep(1)

# that resets Arduino, so first we wait to receive initializing string from Arduino
print ser.readline().strip()

# Now wait for a key press to acquire the data:
raw_input("Press Enter to Acquire...")

# Now we can send our acquire data signal:
nrun=3
dt = 1
ser.write('a ' + str(nrun) + " " + str(dt))

# first line is the length of the payload:
nsamp = int(ser.readline().strip())
nrun  = int(ser.readline().strip())

xl = np.zeros((nrun,nsamp), dtype=float)
yl = np.zeros((nrun,nsamp), dtype=float)

print "receiving payload from Arduion of length ", nsamp, " x ", nrun, "\n";


for i in range(nrun):
    for j in range(nsamp):
        str = ser.readline().strip()
        # print str
        x,y = str.split()
        if ((i<5) and (j<5)):
            print "x: ", x, "y: ", y
        xl[i][j] = x;
        yl[i][j] = y;

ser.close();

for i in range(nrun):
    if (i<5):
        plt.plot(xl[i], yl[i])


np.savetxt('waveform.txt', np.column_stack((xl,yl)))

plt.xlabel("time [milliseconds]")
plt.show();

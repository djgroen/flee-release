import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


def read_datafile(file_name):
  # the skiprows keyword is for heading, but I don't know if trailing lines
  # can be specified
  data = np.loadtxt(file_name, delimiter=',', skiprows=1)
  return data

data = read_datafile("filename.csv")

x = data[:,0] # time
y = data[:,1] # camp 22 (Mahama)
z = data[:,2] # third column for comparison

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.set_title("Title")
ax1.set_xlabel('Time')
ax1.set_ylabel('No. of Refugees')

ax1.plot(x,y, c='r')
ax1.plot(x,z, c='b')

leg = ax1.legend()

plt.show()


# no text should be in csv file except the first row (title)
# change filename.csv & Title to specific one

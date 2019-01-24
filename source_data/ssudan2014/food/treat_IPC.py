import csv
import numpy as np
import pandas as pd

IPC=pd.read_csv("%IPC3.csv")
IPC=IPC.rename(index=str, columns={"Unnamed: 0": "Dates"})
i=1
index=i

while i<len(IPC.index):
  diff=(IPC.ix[i]-IPC.ix[i-1])
  if not diff[1:len(diff)].any():
    IPC=IPC.drop(str(index))
  else:
    i=i+1
  index=index+1

print(IPC)
IPC.to_csv("IPC.csv",index=False)

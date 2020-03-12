import csv
import numpy as np
import pandas as pd

def initiate_food():
  critict=pd.read_csv("flee/source_data/ssudan2014/food/%IPC3.csv")["Unnamed: 0"]
  IPC_all=pd.read_csv("flee/source_data/ssudan2014/food/%IPC3.csv",index_col=0)
  current_i=0

  return [critict,IPC_all,current_i]

def line42day(t,current_i):
  current_critict=critict[current_i]
  while current_critict<t:
    current_i=current_i+1
    current_critict=critict[current_i]
  return current_critict

def updateIPC(self,line_IPC):                		 #to be executed on the ecosystem
  for i in range(0,len(self.locationNames)):
    if not self.locations[i].foreign:		         #needed??
      self.locations[i].IPC=IPC_all.loc[line_IPC,self.region]

def updateMC(self):					 #to be executed on the ecosystem
  for i in range(0,len(self.locationNames)):
    if not self.locations[i].foreign:                       #needed??
      if not self.locations[i].conflict and not self.locations[i].camp:
        self.locations[i].movechance=self.locations[i].IPC/100

def update_IPC_MC(self,line_IPC):			 #maybe better (less computation time)
  for i in range(0,len(self.locationNames)):
    if not self.locations[i].foreign:                       #needed??
      self.locations[i].IPC=IPC_all.loc[line_IPC,self.region]
      if not self.locations[i].conflict and not self.locations[i].camp:
        self.locations[i].movechance=self.locations[i].IPC/100

if __name__ == "__main__":

  [critict,IPC_all,current_i]=initiate_food() #has to go in the main part of flee before starting time count

  for t in range(0,end_time):
    line_IPC=line42day(t,current_i)           #has to go in the time count of flee to choose the values of IPC according to t
    e.update_IPC_MC(line_IPC)                 #update all locations in the ecosystem: IPC indexes and movechances (inside t loop)

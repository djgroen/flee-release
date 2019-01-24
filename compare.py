import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def compare(out_dir_1,out_dir_2):

  food=pd.read_csv("%s/out.csv"%(out_dir_1))
  flee=pd.read_csv("%s/out.csv"%(out_dir_2))
  cols=['Day', 'Tierkidi sim', 'Tierkidi error', 'Pugnido sim', 'Pugnido error', 'Jewi sim', 'Jewi error', 'Kule sim', 'Kule error', 'Kakuma sim', 'Kakuma error', 'Khartoum sim', 'Khartoum error', 'West_Kordofan sim', 'West_Kordofan error', 'Adjumani sim', 'Adjumani error', 'Rhino sim', 'Rhino error', 'Kiryandongo sim', 'Kiryandongo error', 'Total error', 'refugees in camps (simulation)', 'refugee_debt']
  comp=pd.DataFrame(index=flee.index,columns=cols)
  comp["Day"]=flee["Day"]

  for i in cols[1:len(cols)]:
    comp[i]=flee[i]-food[i]
    plt.plot(comp["Day"],comp[i],'b',label="Flee - Food")
    plt.plot(comp["Day"],food[i],'r',label="Food")
    plt.plot(comp["Day"],flee[i],'g',label="Flee")
    plt.plot([0,len(comp["Day"])],[0,0],'k--')
    plt.ylabel("flee - food")
    plt.title(i)
    plt.tight_layout()
    spl=i.split()
    if len(spl)==2:
      if spl[1]=="error":
        plt.ylabel("Error")
      elif spl[1]=="sim":
        plt.ylabel("Number of refugees")
    else:
      plt.ylabel("Number of refugees")
    plt.legend()
    name=spl[0]
    for j in range(len(spl)-1):
      name=name+"_"+spl[j+1]
    plt.savefig("%s/comparison/%s.png"%(out_dir_1,name))
    plt.clf()

  comp.to_csv("%s/comparison/table.csv"%(out_dir_1))


if __name__ == "__main__":
  out_dir_1=sys.argv[1]
  out_dir_2=sys.argv[2]
  compare(out_dir_1,out_dir_2)

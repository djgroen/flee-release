import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import sys
import datamanager.handle_refugee_data as handle_refugee_data

def set_margins(l=0.13,b=0.13,r=0.96,t=0.96):
  #adjust margins. 
  fig = plt.gcf()
  fig.subplots_adjust(bottom=b,top=t,left=l,right=r)


def plotme(out_dir, data, name):

  plt.clf()

  data_x = []
  data_y = []

  d = handle_refugee_data.DataTable("mali2012/refugees.csv", csvformat="mali-portal")

  for day in range(0, len(data["%s data" % name])):
    if d.is_interpolated(name, day) == False:
      #draw a point
      data_x.append(day)
      data_y.append(data.at[day,"%s data" % name])

  # data.loc[:,["%s sim" % name,"%s data" % name]]).as_matrix()
  y1 = data["%s sim" % name].as_matrix()
  y2 = data["%s data" % name].as_matrix()
  days = np.arange(len(y1))

  #plt.ylabel("Number of refugees")
  plt.xlabel("Days elapsed")
  #matplotlib.rc('xtick', labelsize=16) 
  #matplotlib.rc('ytick', labelsize=16) 


  matplotlib.rcParams.update({'font.size': 22})

  country = {"Bobo-Dioulasso":"(BF)","Mentao":"(BF)","Mbera":"(MAU)","Fassala":"(MAU)","Abala":"(NI)","Mangaize":"(NI)","Niamey":"(NI)","Tabareybarey":"(NI)"}

  labelsim, = plt.plot(days,y1, linewidth=10, label="%s %s simulation" % (name.title(), country[name.title()]))
  labeldata, = plt.plot(days,y2, linewidth=10, label="%s %s UNHCR data" % (name.title(), country[name.title()]))
  plt.plot(data_x,data_y,'ob')

  plt.legend(handles=[labelsim, labeldata],loc=4,prop={'size':20})

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)
  #adjust margins. 
  set_margins()

  fig.savefig("%s/%s.png" % (out_dir, name))

def plotme_minimal(out_dir, data, name):

  plt.clf()

  data_x = []
  data_y = []

  d = handle_refugee_data.DataTable("mali2012/refugees.csv", csvformat="mali-portal")

  for day in range(0, len(data["%s data" % name])):
    if d.is_interpolated(name, day) == False:
      #draw a point
      data_x.append(day)
      data_y.append(data.at[day,"%s data" % name])

  # data.loc[:,["%s sim" % name,"%s data" % name]]).as_matrix()
  y1 = data["%s sim" % name].as_matrix()
  y2 = data["%s data" % name].as_matrix()
  days = np.arange(len(y1))

  #plt.ylabel("Number of refugees")
  #plt.xlabel("Days elapsed")
  #matplotlib.rc('xtick', labelsize=16) 
  #matplotlib.rc('ytick', labelsize=16) 


  matplotlib.rcParams.update({'font.size': 28})

  country = {"Bobo-Dioulasso":"(BF)","Mentao":"(BF)","Mbera":"(MAU)","Fassala":"(MAU)","Abala":"(NI)","Mangaize":"(NI)","Niamey":"(NI)","Tabareybarey":"(NI)"}

  max_val = max([max(y1),max(y2)])

  plt.xticks([])
  plt.yticks([2000,5000])
  plt.ylim([0, 1.1*max_val])

  labelsim, = plt.plot(days,y1, linewidth=10, label="%s %s simulation" % (name.title(), country[name.title()]))
  labeldata, = plt.plot(days,y2, linewidth=10, label="%s %s UNHCR data" % (name.title(), country[name.title()]))
  plt.plot(data_x,data_y,'ob')

  #plt.legend(handles=[labelsim, labeldata],loc=4,prop={'size':20})
  plt.gca().legend_ = None
  
  plt.text(295, 0.02*plt.ylim()[1], "%s %s" % (name.title(), country[name.title()]), size=24, ha='right')
  #plt.text(200, 0.02*plt.ylim()[1], "Max: %s" % (max(y1)), size=24)

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(8, 6)
  #adjust margins. 
  set_margins(l=0.14,b=0.13,r=0.96,t=0.96)

  fig.savefig("%s/min-%s.png" % (out_dir, name))


if __name__ == "__main__":

  if len(sys.argv)>1:
    out_dir = sys.argv[1]
  else:
    out_dir = "out"

  matplotlib.style.use('ggplot')
  #figsize=(15, 10)

  refugee_data = pd.read_csv("%s/out.csv" % (out_dir), sep=',', encoding='latin1',index_col='Day')

  for i in ["Mbera","Fassala","Mentao","Bobo-Dioulasso","Abala","Mangaize","Niamey","Tabareybarey"]:
    plotme(out_dir, refugee_data,i)
    plotme_minimal(out_dir, refugee_data,i)

  matplotlib.rcParams.update({'font.size': 20})

  plt.clf()  
  diffdata = refugee_data.loc[:,["Total error"]].as_matrix()
  plt.plot(np.arange(len(diffdata)), diffdata, linewidth=5)
  #plt.legend(handles=[labeldiff],loc=2,prop={'size':14})

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)

  plt.ylabel("Averaged relative difference")
  plt.xlabel("Days elapsed")

  set_margins()
  plt.savefig("%s/error.png" % out_dir)

  refugee_data.loc[:,["refugees in camps (simulation)","refugees in camps (UNHCR)"]].plot(linewidth=5)

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)

  set_margins()
  plt.savefig("%s/numagents.png" % out_dir)

  #plt.show()

#  ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))

#  ts = ts.cumsum()

#  ts.plot()

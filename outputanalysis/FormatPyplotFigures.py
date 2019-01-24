import matplotlib
import matplotlib.pyplot as plt

def set_margins(l=0.13,b=0.13,r=0.96,t=0.96):
  #adjust margins - Setting margins for graphs
  fig = plt.gcf()
  fig.subplots_adjust(bottom=b,top=t,left=l,right=r)

def prepare_figure(xlabel="Days elapsed",ylabel="Number of refugees"):
  #prepares and formats a basic flee visualization figure.
  plt.clf()
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)

  matplotlib.rcParams.update({'font.size': 20})
  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)
  set_margins()
  return fig

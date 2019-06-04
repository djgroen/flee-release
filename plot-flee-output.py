import pandas as pd
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np
import sys
import datamanager.handle_refugee_data as handle_refugee_data
import warnings
import outputanalysis.analysis as a

warnings.filterwarnings("ignore")


"""
This is a generic plotting program.
See an example of the output format used in test-output/out.csv
Example use:
  python3 plot-flee-output.py test-output
"""

class LocationErrors:
  """
  Class containing a dictionary of errors and diagnostics pertaining a single location.
  """
  def __init__(self):
    self.errors = {}


class SimulationErrors:
  """
  Class containing all error measures within a single simulation.
  It should be initialized with a Python list of the LocationErrors structure
  for all of the relevant locations.
  """
  def __init__(self, location_errors):
    self.location_errors = location_errors


  def abs_diff(self, rescaled=True):
    #true_total_refs is the number of total refugees according to the data.

    errtype = "absolute difference"
    if rescaled:
      errtype = "absolute difference rescaled"

    self.tmp = self.location_errors[0].errors[errtype]

    for lerr in self.location_errors[1:]:
      self.tmp = np.add(self.tmp, lerr.errors[errtype])

    return self.tmp

  def get_error(self, err_type):
    """
    Here err_type is the string name of the error that needs to be aggregated.
    """
    self.tmp = self.location_errors[0].errors[err_type] * self.location_errors[0].errors["N"]
    N = self.location_errors[0].errors["N"]

    for lerr in self.location_errors[1:]:
      self.tmp = np.add(self.tmp, lerr.errors[err_type] * lerr.errors["N"])
      N += lerr.errors["N"]

    #print(self.tmp, N, self.tmp/ N)
    return self.tmp / N

def set_margins(l=0.13,b=0.13,r=0.96,t=0.96):
  #adjust margins - Setting margins for graphs
  fig = plt.gcf()
  fig.subplots_adjust(bottom=b,top=t,left=l,right=r)


def plotme(out_dir, data, name, offset=0, legend_loc=4, naieve_model=True):
  """
  Advanced plotting function for validation of refugee registration numbers in camps.
  """
  plt.clf()

  # data.loc[:,["%s sim" % name,"%s data" % name]]).as_matrix()
  y1 = data["%s sim" % name].as_matrix()

  y2 = data["%s data" % name].as_matrix()
  days = np.arange(len(y1))

  naieve_early_day = 7
  naieve_training_day = 30

  #print(name, offset, len(y1), len(y2))
  plt.xlabel("Days elapsed")

  matplotlib.rcParams.update({'font.size': 20})

  #Plotting lines representing simulation results.
  if offset == 0:
      labelsim, = plt.plot(days,y1, linewidth=8, label="%s simulation" % (name.title()))
  if offset > 0:
      labelsim, = plt.plot(days[:-offset],y1[offset:], linewidth=8, label="%s simulation" % (name.title()))

  # Plotting line representing UNHCR data.
  labeldata, = plt.plot(days,y2, 'o-', linewidth=8, label="%s UNHCR data" % (name.title()))

  # Add label for the naieve model if it is enabled.
  plt.legend(handles=[labelsim, labeldata],loc=legend_loc,prop={'size':18})

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)
  #adjust margins
  set_margins()

  if offset == 0:
      fig.savefig("%s/%s-%s.png" % (out_dir, name, legend_loc))
  else:
      fig.savefig("%s/%s-offset-%s.png" % (out_dir, name, offset))

  # Rescaled values
  plt.clf()

  plt.xlabel("Days elapsed")
  plt.ylabel("Number of refugees")

  simtot = data["refugees in camps (simulation)"].as_matrix().flatten()
  untot = data["refugees in camps (UNHCR)"].as_matrix().flatten()

  y1_rescaled = np.zeros(len(y1))
  for i in range(0, len(y1_rescaled)):
      # Only rescale if simtot > 0
      if simtot[i] > 0:
          y1_rescaled[i] = y1[i] * untot[i] / simtot[i]


  labelsim, = plt.plot(days,y1_rescaled, linewidth=8, label="%s simulation" % (name.title()))

  labeldata, = plt.plot(days,y2, linewidth=8, label="%s UNHCR data" % (name.title()))

  # Plotting line representing naieve model
  if naieve_model:
      # Flat line from day 7
      n1 = np.empty(len(days))
      n1.fill(y2[naieve_early_day])
      # Flat line from day 30
      n2 = np.empty(len(days))
      n2.fill(y2[naieve_training_day])
      # Sloped line from day 7
      n3 = np.empty(len(days))
      n3.fill(y2[naieve_early_day])
      for i in range(0,len(n3)):
        if y2[naieve_early_day] > 0:
          n3[i] *= i*y2[naieve_early_day]/y2[naieve_early_day]
        else:
          n3[i] = 0
      # Sloped line from day 30
      n4 = np.empty(len(days))
      n4.fill(y2[naieve_training_day])
      for i in range(0,len(n4)):
        if y2[naieve_early_day] > 0:
          n4[i] *= i*y2[naieve_training_day]/y2[naieve_training_day]
        else:
          n4[i] = 0
      # Flat ratio from day 7
      n5 = np.empty(len(days))
      for i in range(0,len(n5)):
        n5[i] = untot[i] * (y2[naieve_early_day] / untot[naieve_early_day])
      # Flat ratio from day 7
      n6 = np.empty(len(days))
      for i in range(0,len(n6)):
        n6[i] = untot[i] * (y2[naieve_training_day] / untot[naieve_training_day])

      labelnaieve, = plt.plot(days, n1, linewidth=6, label="%s naieve model" % (name.title()))
      labelnaieve, = plt.plot(days, n2, linewidth=6, label="%s naieve early" % (name.title()))
      plt.axvline(x=naieve_early_day, linewidth=2, ls="dotted", c="grey")
      plt.axvline(x=naieve_training_day, linewidth=2, ls="dotted", c="grey")


  if naieve_model:
      plt.legend(handles=[labelsim, labelnaieve, labeldata],loc=legend_loc,prop={'size':18})
  else:
      plt.legend(handles=[labelsim, labeldata],loc=legend_loc,prop={'size':18})

  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)
  #adjust margins
  set_margins()

  if naieve_model:
    fig.savefig("%s/%s-%s-rescaled-N.png" % (out_dir, name, legend_loc))
  else:
    fig.savefig("%s/%s-%s-rescaled.png" % (out_dir, name, legend_loc))


  """
  Error quantification phase:
  - At the end of the plotme command we wish to quantify the errors and mismatches for this camp.
  """

  lerr = LocationErrors()

  if offset > 0:
    y1 = y1[offset:]
    y1_rescaled = y1_rescaled[offset:]
    y2 = y2[:-offset]
    untot = untot[:-offset]

  # absolute difference
  lerr.errors["absolute difference"] = a.abs_diffs(y1, y2)

  # absolute difference (rescaled)
  lerr.errors["absolute difference rescaled"] = a.abs_diffs(y1_rescaled, y2)
  

  # ratio difference
  lerr.errors["ratio difference"] = a.abs_diffs(y1, y2) / (np.maximum(untot, np.ones(len(untot))))

  """ Errors of which I'm usure whether to report:
   - accuracy ratio (forecast / true value), because it crashes if denominator is 0.
   - ln(accuracy ratio).
  """

  # We can only calculate the Mean Absolute Scaled Error if we have a naieve model in our plot.
  if naieve_model:

    # Number of observations (aggrgate refugee days in UNHCR data set for this location)
    lerr.errors["N"] = np.sum(y2)

    # flat naieve model (7 day)
    lerr.errors["MASE7"] = a.calculate_MASE(y1_rescaled, y2, n1, naieve_early_day)
    lerr.errors["MASE7-sloped"] = a.calculate_MASE(y1_rescaled, y2, n3, naieve_early_day)
    lerr.errors["MASE7-ratio"] = a.calculate_MASE(y1_rescaled, y2, n5, naieve_early_day)

    # flat naieve model (30 day)
    lerr.errors["MASE30"] = a.calculate_MASE(y1_rescaled, y2, n2, naieve_training_day)
    lerr.errors["MASE30-sloped"] = a.calculate_MASE(y1_rescaled, y2, n4, naieve_training_day)
    lerr.errors["MASE30-ratio"] = a.calculate_MASE(y1_rescaled, y2, n6, naieve_training_day)


    # Accuracy ratio doesn't work because of 0 values in the data.
    #ln_accuracy_ratio = calculate_ln_accuracy_ratio(y1, y2)
    #ln_accuracy_ratio_30 = calculate_ln_accuracy_ratio(y1[30:], y2[30:])
    #print(out_dir, name, "MASE7: ", lerr.errors["MASE7"], ", MASE30: ", lerr.errors["MASE30"], ", abs. diff. 30: ", np.mean(lerr.errors["absolute difference"]))
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (out_dir, name, lerr.errors["MASE7"],lerr.errors["MASE7-sloped"], lerr.errors["MASE7-ratio"],lerr.errors["MASE30"],lerr.errors["MASE30-sloped"],lerr.errors["MASE30-ratio"],lerr.errors["N"]))

  return lerr




def plotme_minimal(out_dir, data, name):
  """
  Explaining minimal graphs: populating data points to generate graphs and an example
  """

  plt.clf()

  data_x = []
  data_y = []

  d = handle_refugee_data.DataTable("mali2012/refugees.csv", csvformat="mali-portal")

  #Loop - taking the length of dataset for x and y rays
  for day in range(0, len(data["%s data" % name])):
    if d.is_interpolated(name, day) == False:
      #draw a point
      data_x.append(day)
      data_y.append(data.at[day,"%s data" % name])

  # data.loc[:,["%s sim" % name,"%s data" % name]]).as_matrix()
  y1 = data["%s sim" % name].as_matrix()
  y2 = data["%s data" % name].as_matrix()
  days = np.arange(len(y1))

  matplotlib.rcParams.update({'font.size': 18})

  max_val = max([max(y1),max(y2)])

  #Graph labels
  plt.xticks([])
  plt.yticks([2000,5000])
  plt.ylim([0, 1.1*max_val])

  #Plotting lines representing simulation results and UNHCR data
  labelsim, = plt.plot(days,y1, linewidth=10, label="%s simulation" % (name.title()))
  labeldata, = plt.plot(days,y2, linewidth=10, label="%s UNHCR data" % (name.title()))
  plt.plot(data_x,data_y,'ob')


  #Text labels
  #plt.legend(handles=[labelsim, labeldata],loc=4,prop={'size':20})
  plt.gca().legend_ = None

  plt.text(295, 0.02*plt.ylim()[1], "%s" % (name.title()), size=24, ha='right')
  #plt.text(200, 0.02*plt.ylim()[1], "Max: %s" % (max(y1)), size=24)

  #Size of plots/graphs
  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(7, 6)
  #adjust margins.
  set_margins(l=0.14,b=0.13,r=0.96,t=0.96)

  fig.savefig("%s/min-%s.png" % (out_dir, name))




#Start of the code, assuring arguments of out-folder & csv file are kept
if __name__ == "__main__":

  if len(sys.argv)>1:
    in_dir = sys.argv[1]
  else:
    in_dir = "out"

  if len(sys.argv)>2:
    out_dir = sys.argv[2]
  else:
    out_dir = "out"

  matplotlib.style.use('ggplot')
  #figsize=(15, 10)

  refugee_data = pd.read_csv("%s/out.csv" % (in_dir), sep=',', encoding='latin1',index_col='Day')

  #Identifying location names for graphs
  rd_cols = list(refugee_data.columns.values)
  location_names = []
  for i in rd_cols:
    if " sim" in i:
      if "numAgents" not in i:
        location_names.append(' '.join(i.split()[:-1]))


  #Plotting and saving numagents (total refugee numbers) graph
  #TODO: These labels need to be more flexible/modifiable.

  plt.xlabel("Days elapsed")

  matplotlib.rcParams.update({'font.size': 20})


  if "refugee_debt" in refugee_data.columns:
    refugee_data.loc[:,["total refugees (simulation)","refugees in camps (simulation)","raw UNHCR refugee count","refugee_debt"]].plot(linewidth=5)
  else:
    refugee_data.loc[:,["total refugees (simulation)","refugees in camps (UNHCR)","raw UNHCR refugee count"]].plot(linewidth=5)

  #Size of plots/figures
  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)

  set_margins()
  plt.savefig("%s/numagents.png" % out_dir)


  # Calculate the best offset.

  sim_refs = refugee_data.loc[:,["refugees in camps (simulation)"]].as_matrix().flatten()
  un_refs = refugee_data.loc[:,["refugees in camps (UNHCR)"]].as_matrix().flatten()
  raw_refs = refugee_data.loc[:,["raw UNHCR refugee count"]].as_matrix().flatten()

  """
  offset = 0

  min_error = 1000000
  error_at_zero_offset = 0

  for i in range(0,200):
      compare_len = len(sim_refs[i:])
      error = np.mean(np.abs(sim_refs[i:] - raw_refs[:compare_len]))

      if i == 0:
        error_at_zero_offset = error

      #print("error with offset ", i, " is: ", error)
      if error < min_error:
        min_error = error
        offset = i

  print(out_dir, ": The best offset = ", offset, ", error = ", min_error, ", error at offset 0 = ",error_at_zero_offset)
  """

  PlotOffsets = True

  # Plots for all locations, one .png file for every time plotme is called.
  # Also populated LocationErrors classes.

  loc_errors = []
  nmodel = False

  for i in location_names:
      loc_errors.append(plotme(out_dir, refugee_data, i, legend_loc=4, naieve_model=nmodel))
      #plotme(out_dir, refugee_data, i, legend_loc=1)

      #plotme(out_dir, refugee_data, i, legend_loc=4, naieve_model=nmodel)
      #loc_errors.append(plotme(out_dir, refugee_data, i, legend_loc=4, naieve_model=True))

  sim_errors = SimulationErrors(loc_errors)
  #print(sim_errors.abs_diff())
  if nmodel:
    print("%s & %s & %s & %s & %s & %s & %s\\\\" % (out_dir, sim_errors.get_error("MASE7"), sim_errors.get_error("MASE7-sloped"),sim_errors.get_error("MASE7-ratio"),sim_errors.get_error("MASE30"),sim_errors.get_error("MASE30-sloped"),sim_errors.get_error("MASE30-ratio")))

  matplotlib.rcParams.update({'font.size': 20})

  plt.clf()

  # ERROR PLOTS

  #Size of plots/figures
  fig = matplotlib.pyplot.gcf()
  fig.set_size_inches(12, 8)

  #Plotting and saving error (differences) graph
  plt.ylabel("Averaged relative difference")
  plt.xlabel("Days elapsed")

  diffdata = sim_errors.abs_diff(rescaled=False) / np.maximum(un_refs, np.ones(len(un_refs)))
  diffdata_rescaled = sim_errors.abs_diff() / np.maximum(un_refs, np.ones(len(un_refs)))
  print(out_dir,": Averaged error normal: ", np.mean(diffdata), ", rescaled: ", np.mean(diffdata_rescaled),", len: ", len(diffdata))

  #labeldiff, = plt.plot(np.arange(len(diffdata)), diffdata, linewidth=5, label="error (not rescaled)")
  labeldiff2, = plt.plot(np.arange(len(diffdata_rescaled)), diffdata_rescaled, linewidth=5, label="error")
  #labeldiff2, = plt.plot(np.arange(len(diffdata)), ref_mismatch_error, linewidth=5, label="total refugee difference")

  plt.legend(handles=[labeldiff2],loc=1,prop={'size':14})

  set_margins()
  plt.savefig("%s/error.png" % out_dir)

  labeldiff, = plt.plot(np.arange(len(diffdata)), diffdata, linewidth=5, label="error (not rescaled)")
  plt.legend(handles=[labeldiff, labeldiff2],loc=1,prop={'size':14})

  set_margins()
  plt.savefig("%s/error-comparison.png" % out_dir)

  plt.clf()


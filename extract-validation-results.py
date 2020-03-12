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

def plotme(data, name, naieve_model=True):
  """
  Advanced plotting function for validation of refugee registration numbers in camps.
  """

  # data.loc[:,["%s sim" % name,"%s data" % name]]).as_matrix()
  y1 = data["%s sim" % name].as_matrix()

  y2 = data["%s data" % name].as_matrix()
  days = np.arange(len(y1))

  naieve_early_day = 7
  naieve_training_day = 30

  simtot = data["refugees in camps (simulation)"].as_matrix().flatten()
  untot = data["refugees in camps (UNHCR)"].as_matrix().flatten()

  y1_rescaled = np.zeros(len(y1))
  for i in range(0, len(y1_rescaled)):
      # Only rescale if simtot > 0
      if simtot[i] > 0:
          y1_rescaled[i] = y1[i] * untot[i] / simtot[i]

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

  """
  Error quantification phase:
  - At the end of the plotme command we wish to quantify the errors and mismatches for this camp.
  """

  lerr = LocationErrors()

  # absolute difference
  lerr.errors["absolute difference"] = a.abs_diffs(y1, y2)
  lerr.errors["absolute difference ave"] = np.mean(lerr.errors["absolute difference"])

  # absolute difference (rescaled)
  lerr.errors["absolute difference rescaled"] = a.abs_diffs(y1_rescaled, y2)
  lerr.errors["absolute difference rescaled ave"] = np.mean(lerr.errors["absolute difference rescaled"])
  

  # ratio difference
  lerr.errors["ratio difference"] = a.abs_diffs(y1, y2) / (np.maximum(untot, np.ones(len(untot))))
  lerr.errors["ratio difference ave"] = np.mean(lerr.errors["ratio difference"])

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

    print("  %s:\n    mase7: %s\n    mase7-sloped: %s\n    mase7-ratio: %s\n    mase30: %s\n    mase30-sloped: %s\n    mase30-ratio: %s\n    N: %s" % (name, lerr.errors["MASE7"],lerr.errors["MASE7-sloped"], lerr.errors["MASE7-ratio"],lerr.errors["MASE30"],lerr.errors["MASE30-sloped"],lerr.errors["MASE30-ratio"],lerr.errors["N"]))
    print("    absolute difference ave: {absolute difference ave}\n    absolute difference rescaled ave: {absolute difference rescaled ave}\n    ratio difference ave: {ratio difference ave}".format(**lerr.errors))
    #print("  absolute difference: {absolute difference}\n  absolute difference rescaled: {absolute difference rescaled}\n  ratio difference: {ratio difference}".format(**lerr.errors))

  return lerr


#Start of the code, assuring arguments of out-folder & csv file are kept
if __name__ == "__main__":

  if len(sys.argv)>1:
    in_dir = sys.argv[1]
  else:
    in_dir = "out"

  refugee_data = pd.read_csv("%s/out.csv" % (in_dir), sep=',', encoding='latin1',index_col='Day')

  #Identifying location names for graphs
  rd_cols = list(refugee_data.columns.values)
  location_names = []
  for i in rd_cols:
    if " sim" in i:
      if "numAgents" not in i:
        location_names.append(' '.join(i.split()[:-1]))


  if "refugee_debt" in refugee_data.columns:
    refugee_data.loc[:,["total refugees (simulation)","refugees in camps (simulation)","raw UNHCR refugee count","refugee_debt"]].plot(linewidth=5)
  else:
    refugee_data.loc[:,["total refugees (simulation)","refugees in camps (UNHCR)","raw UNHCR refugee count"]].plot(linewidth=5)

  # Calculate the best offset.

  sim_refs = refugee_data.loc[:,["refugees in camps (simulation)"]].as_matrix().flatten()
  un_refs = refugee_data.loc[:,["refugees in camps (UNHCR)"]].as_matrix().flatten()
  raw_refs = refugee_data.loc[:,["raw UNHCR refugee count"]].as_matrix().flatten()

  # Plots for all locations, one .png file for every time plotme is called.
  # Also populated LocationErrors classes.

  loc_errors = []
  nmodel = True

  print("measurements:")
  for i in location_names:
      loc_errors.append(plotme(refugee_data, i, naieve_model=nmodel))

  sim_errors = SimulationErrors(loc_errors)
  
  print("input directory: {}".format(in_dir))

  print("totals:")
  if nmodel:
    print("  mase7: %s\n  mase7-sloped: %s\n  mase7-ratio: %s\n  mase30: %s\n  mase30-sloped: %s\n  mase30-ratio: %s" % (sim_errors.get_error("MASE7"), sim_errors.get_error("MASE7-sloped"), sim_errors.get_error("MASE7-ratio"), sim_errors.get_error("MASE30"), sim_errors.get_error("MASE30-sloped"), sim_errors.get_error("MASE30-ratio")))
    #print("%s & %s & %s & %s & %s & %s & %s\\\\" % (in_dir, sim_errors.get_error("MASE7"), sim_errors.get_error("MASE7-sloped"),sim_errors.get_error("MASE7-ratio"),sim_errors.get_error("MASE30"),sim_errors.get_error("MASE30-sloped"),sim_errors.get_error("MASE30-ratio")))

  diffdata = sim_errors.abs_diff(rescaled=False) / np.maximum(un_refs, np.ones(len(un_refs)))
  diffdata_rescaled = sim_errors.abs_diff() / np.maximum(un_refs, np.ones(len(un_refs)))
  print("  Error (normal): {}\n  Error (rescaled): {}\n  Simulation Period: {}".format(np.mean(diffdata), np.mean(diffdata_rescaled), len(diffdata)))


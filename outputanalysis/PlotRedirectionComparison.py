#This script should be run using the main flee directory as working directory.
#TODO: Rewrite this to create a redirection comparison.

import pandas as pd
import matplotlib
matplotlib.use('Pdf')
import matplotlib.pyplot as plt
import numpy as np
import sys
import warnings
import analysis as a

import StoreDiagnostics as dd
import FormatPyplotFigures as fpf
import CalculateDiagnostics

warnings.filterwarnings("ignore")


def compare_numagents_camp(out_dir, datas, name, legend_loc=4):
  """
  Advanced plotting function for validation of refugee registration numbers in camps.
  """
  fig = fpf.prepare_figure(xlabel="Days elapsed")

  labelssim = []

  n=0
  for data in datas:
    y1 = data["%s sim" % name].as_matrix()

    y2 = data["%s data" % name].as_matrix()
    days = np.arange(len(y1))

    #Plotting lines representing simulation results.
    labelsim, = plt.plot(days,y1, linewidth=8, label="%s" % (names[n]))
    labelssim.append(labelsim)
    n+=1

  # Add label for the naieve model if it is enabled.
  plt.legend(handles=labelssim,loc=legend_loc,prop={'size':18})

  fig.savefig("%s/%s-%s.png" % (out_dir, name, legend_loc))

  # Rescaled values
  plt.clf()

  fig = fpf.prepare_figure(xlabel="Days elapsed")

  plt.xlabel("Days elapsed")
  plt.ylabel("Number of refugees")

  labelssim = []

  n=0
  for data in datas:
    y1 = data["%s sim" % name].as_matrix()
    days = np.arange(len(y1))

    simtot = data["refugees in camps (simulation)"].as_matrix().flatten()
    untot = data["refugees in camps (UNHCR)"].as_matrix().flatten()

    #print(y1,simtot,untot)

    y1_rescaled = np.zeros(len(y1))
    for i in range(0, len(y1_rescaled)):
      # Only rescale if simtot > 0
      if simtot[i] > 0:
        y1_rescaled[i] = y1[i] * untot[i] / simtot[i]

    print(y1_rescaled)

    labelsim, = plt.plot(days, y1_rescaled, linewidth=8, label="%s" % (names[n]))
    labelssim.append(labelsim)
    n += 1
    #labeldata, = plt.plot(days, y1, linewidth=8, label="%s UNHCR data" % (name.title()))


  plt.legend(handles=labelssim,loc=legend_loc,prop={'size':18})


  fig.savefig("%s/%s-%s-rescaled.png" % (out_dir, name, legend_loc))




#Start of the code, assuring arguments of out-folder & csv file are kept
if __name__ == "__main__":


  in_dirs = []
  names = []

  for i in range(1, len(sys.argv)-1):
    in_dirs.append(sys.argv[i])
    names.append(sys.argv[i])

  out_dir = sys.argv[-1]

  matplotlib.style.use('ggplot')
  #figsize=(15, 10)

  refugee_data = []

  print(in_dirs)

  for d in in_dirs:
    refugee_data.append(pd.read_csv("%s/out.csv" % (d), sep=',', encoding='latin1',index_col='Day'))

  #Identifying location names for graphs
  rd_cols = list(refugee_data[0].columns.values)
  location_names = []
  for i in rd_cols:
    if " sim" in i:
      if "numAgents" not in i:
        location_names.append(' '.join(i.split()[:-1]))


  plt.xlabel("Days elapsed")

  # Calculate the best offset.

  sim_refs = []
  un_refs = []
  raw_refs = []


  for i in range(0, len(refugee_data)):
    sim_refs.append(refugee_data[i].loc[:,["refugees in camps (simulation)"]].as_matrix().flatten())
    un_refs.append(refugee_data[i].loc[:,["refugees in camps (UNHCR)"]].as_matrix().flatten())
    raw_refs.append(refugee_data[i].loc[:,["raw UNHCR refugee count"]].as_matrix().flatten())

  loc_errors = []
  sim_errors = []
  nmodel = False

  #plot numagents compare by camp.
  for i in location_names:
    compare_numagents_camp(out_dir, refugee_data, i, legend_loc=4)

  for i in range(0, len(refugee_data)):
    loc_errors.append([])
    for j in location_names:
      loc_errors[i].append(CalculateDiagnostics.calculate_errors(out_dir, refugee_data[i], j, naieve_model=nmodel))

    sim_errors.append(dd.SimulationErrors(loc_errors[i]))

  matplotlib.rcParams.update({'font.size': 20})

  plt.clf()

  # ERROR PLOTS

  #Size of plots/figures
  fig = fpf.prepare_figure()

  #Plotting and saving error (differences) graph
  plt.ylabel("Averaged relative difference")
  plt.xlabel("Days elapsed")

  handle_list = []

  for i in range(0, len(in_dirs)):
    diffdata = (sim_errors[i].abs_diff(rescaled=False) / np.maximum(un_refs[i], np.ones(len(un_refs[i]))))
    diffdata_rescaled = (sim_errors[i].abs_diff() / np.maximum(un_refs[i], np.ones(len(un_refs[i]))))
    print(out_dir,": Averaged error normal: ", np.mean(diffdata), ", rescaled: ", np.mean(diffdata_rescaled),", len: ", len(diffdata))
    plt.plot(np.arange(len(diffdata_rescaled)), diffdata_rescaled, linewidth=5, label="error %s" % names[i])

  plt.legend(loc=1,prop={'size':14})

  plt.savefig("%s/error-compare-runs.png" % out_dir)

  plt.clf()
  fig = fpf.prepare_figure()

  #Plotting and saving error (differences) graph
  plt.ylabel("Number of agents in camps (simulation)")
  plt.xlabel("Days elapsed")

  for i in range(0, len(in_dirs)):
    #refugee_data[i].loc[:,["total refugees (simulation)","refugees in camps (simulation)","raw UNHCR refugee count","refugee_debt"]].plot(linewidth=5, label="refugees in camps (sim) %s" % names[i])
    plt.plot(np.arange(len(un_refs[i])), refugee_data[i].loc[:,["refugees in camps (simulation)"]], linewidth=5, label=names[i])

  plt.legend(loc=1,prop={'size':14})

  plt.savefig("%s/numsim-compare-runs.png" % out_dir)


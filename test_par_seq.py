from flee import flee
from datamanager import handle_refugee_data
from datamanager import DataTable #DataTable.subtract_dates()
from flee import InputGeography
import numpy as np
import outputanalysis.analysis as a
import sys
import argparse
import time

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2010-01-01")


if __name__ == "__main__":

  t_exec_start = time.time()

  end_time = 10
  last_physical_day = 10

  parser = argparse.ArgumentParser(description='Run a parallel Flee benchmark.')
  parser.add_argument("-p", "--parallelmode", type=str, default="advanced",
          help="Parallelization mode (advanced, classic, cl-hilat OR adv-lowlat)")
  parser.add_argument("-N", "--initialagents", type=int, default=100000,
          help="Number of agents at the start of the simulation.")
  parser.add_argument("-d", "--newagentsperstep", type=int, default=1000,
          help="Number of agents added per time step.")
  parser.add_argument("-t", "--simulationperiod", type=int, default=10,
          help="Duration of the simulation in days.")
  parser.add_argument("-i", "--inputdir", type=str, default="test_data/test_input_csv",
          help="Directory with parallel test input. Must have locations named 'A','D','E' and 'F'.")

  args = parser.parse_args()

  end_time = args.simulationperiod
  last_physical_day = args.simulationperiod

  e = flee.Ecosystem()

  if args.parallelmode is "advanced" or "adv-lowlat":
    e.parallel_mode = "loc-par"
  else:
    e.parallel_mode = "classic"

  if args.parallelmode is "advanced" or "cl-hilat":
    e.latency_mode = "high_latency"
  else:
    e.latency_mode = "low_latency"

  print("MODE: ", args, file=sys.stderr)

  ig = InputGeography.InputGeography()

  ig.ReadLocationsFromCSV("%s/locations.csv" % args.inputdir)

  ig.ReadLinksFromCSV("%s/routes.csv" % args.inputdir)

  ig.ReadClosuresFromCSV("%s/closures.csv" % args.inputdir)

  e,lm = ig.StoreInputGeographyInEcosystem(e)

  #print("Network data loaded")

  #d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="test_data/test_input_csv/refugee_data", start_date="2010-01-01", data_layout="data_layout.csv")

  output_header_string = "Day,"

  camp_locations      = e.get_camp_names()

  ig.AddNewConflictZones(e,0)
  # All initial refugees start in location A.
  e.add_agents_to_conflict_zones(args.initialagents)

  for l in camp_locations:
    output_header_string += "%s sim,%s data,%s error," % (lm[l].name, lm[l].name, lm[l].name)


  output_header_string += "Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,refugees in camps (simulation),refugee_debt"

  if e.getRankN(0):
    print(output_header_string)

  # Set up a mechanism to incorporate temporary decreases in refugees
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.

  t_exec_init = time.time()
  if e.getRankN(0):
    my_file = open('perf.log', 'w', encoding='utf-8')
    print("Init time,{}".format(t_exec_init - t_exec_start), file=my_file)

  for t in range(0,end_time):

    if t>0:
      ig.AddNewConflictZones(e,t)

    # Determine number of new refugees to insert into the system.
    new_refs = args.newagentsperstep
    refugees_raw += new_refs

    #Insert refugee agents
    e.add_agents_to_conflict_zones(new_refs)

    e.refresh_conflict_weights()
    t_data = t

    e.enact_border_closures(t)
    e.evolve()

    #Calculation of error terms
    errors = []
    abs_errors = []

    camps = []
    for i in camp_locations:
      camps += [lm[i]]

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents

    output = "%s" % t

    for i in range(0,len(camp_locations)):
      output += ",%s" % (lm[camp_locations[i]].numAgents)

    if refugees_raw>0:
      output += ",%s,%s" % (e.numAgents(), refugees_in_camps_sim)
    else:
      output += ",0,0"

    if e.getRankN(t):
      print(output)

  t_exec_end = time.time()
  if e.getRankN(0):
    my_file = open('perf.log', 'a', encoding='utf-8')
    print("Time in main loop,{}".format(t_exec_end - t_exec_init), file=my_file)

from flee import pflee
from datamanager import handle_refugee_data
from datamanager import DataTable #DataTable.subtract_dates()
from flee import InputGeography
import numpy as np
import outputanalysis.analysis as a
import sys

def AddInitialRefugees(e, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = 1000000
  for i in range(0, num_refugees):
    e.addAgent(location=loc)

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2010-01-01")


if __name__ == "__main__":

  end_time = 10
  last_physical_day = 10

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 10
      last_physical_day = 10
      duration = flee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time

  e = pflee.Ecosystem()

  ig = InputGeography.InputGeography()

  ig.ReadLocationsFromCSV("test_data/test_input_csv/locations.csv")

  ig.ReadLinksFromCSV("test_data/test_input_csv/routes.csv")

  ig.ReadClosuresFromCSV("test_data/test_input_csv/closures.csv")

  e,lm = ig.StoreInputGeographyInEcosystem(e)

  #print("Network data loaded")

  #d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="test_data/test_input_csv/refugee_data", start_date="2010-01-01", data_layout="data_layout.csv")

  output_header_string = "Day,"

  camp_locations      = ["D","E","F"]
  #TODO: Add Camps from CSV based on their location type.

  for l in camp_locations:
    AddInitialRefugees(e,lm[l])
    output_header_string += "%s sim,%s data,%s error," % (lm[l].name, lm[l].name, lm[l].name)

  output_header_string += "Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,refugees in camps (simulation),refugee_debt"

  print(output_header_string)

  # Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.

  for t in range(0,end_time):

    #if t>0:
    ig.AddNewConflictZones(e,t)

    # Determine number of new refugees to insert into the system.
    new_refs = 1000
    refugees_raw += new_refs

    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    #Insert refugee agents
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

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


    print(output)

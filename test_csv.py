from flee import flee
from datamanager import handle_refugee_data
from datamanager import DataTable #DataTable.subtract_dates()
from flee import InputGeography
import numpy as np
import outputanalysis.analysis as a
import sys

def AddInitialRefugees(e, d, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = int(d.get_field(loc.name, 0, FullInterpolation=True))
  for i in range(0, num_refugees):
    e.addAgent(location=loc)

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2010-01-01")


if __name__ == "__main__":

  end_time = 100
  last_physical_day = 100

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 100
      last_physical_day = 100
      duration = flee.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time

  e = flee.Ecosystem()

  ig = InputGeography.InputGeography()

  flee.SimulationSettings.FlareConflictInputFile = "test_data/test_input_csv/flare-out.csv"
  ig.ReadFlareConflictInputCSV(flee.SimulationSettings.FlareConflictInputFile)

  print(ig.conflicts)

  assert ig.conflicts["C"][49] == 0
  assert ig.conflicts["C"][50] == 1

  assert ig.conflicts["A"][0] == 1
  assert ig.conflicts["C2"][94] == 0

  ig.ReadLocationsFromCSV("test_data/test_input_csv/locations.csv")

  ig.ReadLinksFromCSV("test_data/test_input_csv/routes.csv")

  ig.ReadClosuresFromCSV("test_data/test_input_csv/closures.csv")

  e,lm = ig.StoreInputGeographyInEcosystem(e)

  #print("Network data loaded")

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="test_data/test_input_csv/refugee_data", start_date="2010-01-01", data_layout="data_layout.csv")

  output_header_string = "Day,"

  camp_locations      = ["D","E","F"]
  #TODO: Add Camps from CSV based on their location type.

  for l in camp_locations:
    AddInitialRefugees(e,d,lm[l])
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
    new_refs = d.get_daily_difference(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_daily_difference(t, FullInterpolation=True)

    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    #Insert refugee agents
    e.add_agents_to_conflict_zones(new_refs)

    e.refresh_conflict_weights()
    t_data = t

    e.enact_border_closures(t)
    e.evolve()

    #Calculation of error terms
    errors = []
    abs_errors = []
    loc_data = []

    camps = []
    for i in camp_locations:
      camps += [lm[i]]
      loc_data += [d.get_field(i, t)]

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents

    # calculate errors
    j=0
    for i in camp_locations:
      errors += [a.rel_error(lm[i].numAgents, loc_data[j])]
      abs_errors += [a.abs_error(lm[i].numAgents, loc_data[j])]

      j += 1

    output = "%s" % t

    for i in range(0,len(errors)):
      output += ",%s,%s,%s" % (lm[camp_locations[i]].numAgents, loc_data[i], errors[i])

    if refugees_raw>0:
      #output_string += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw)
      output += ",%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, refugees_in_camps_sim, refugee_debt)
    else:
      output += ",0,0,0,0,0,0,0"
      #output_string += ",0"


    print(output)

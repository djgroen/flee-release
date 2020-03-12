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
  return DataTable.subtract_dates(date,"2013-12-15")


if __name__ == "__main__":

  end_time = 604
  last_physical_day = 604

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 604
      last_physical_day = 604
      duration = flee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time

  e = flee.Ecosystem()

  ig = InputGeography.InputGeography()

  ig.ReadLocationsFromCSV("examples/ssudan_input_csv/locations.csv")

  ig.ReadLinksFromCSV("examples/ssudan_input_csv/routes.csv")

  ig.ReadClosuresFromCSV("examples/ssudan_input_csv/closures.csv")

  e,lm = ig.StoreInputGeographyInEcosystem(e)

  #print("Network data loaded")

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="source_data/ssudan2014/", start_date="2013-12-15", data_layout="data_layout.csv")

  #Correcting for overestimations due to inaccurate level 1 registrations in five of the camps.
  #These errors led to a perceived large drop in refugee population in all of these camps.
  #We correct by linearly scaling the values down to make the last level 1 registration match the first level 2 registration value.
  #To our knowledge, all level 2 registration procedures were put in place by the end of 2016.
  d.correctLevel1Registrations("Tierkidi","2014-08-08")
  d.correctLevel1Registrations("Pugnido","2015-06-26")
  d.correctLevel1Registrations("Jewi","2015-07-31")
  d.correctLevel1Registrations("Kule","2014-09-12")
  d.correctLevel1Registrations("Kakuma","2014-06-26")
  d.correctLevel1Registrations("Khartoum","2014-04-27")
  d.correctLevel1Registrations("West_Kordofan","2015-08-05")
  d.correctLevel1Registrations("Rhino","2014-05-21")
  d.correctLevel1Registrations("Kiryandongo","2014-05-27")

  lm["Tierkidi"].capacity = d.getMaxFromData("Tierkidi", last_physical_day)
  lm["Pugnido"].capacity = d.getMaxFromData("Pugnido", last_physical_day)
  lm["Jewi"].capacity = d.getMaxFromData("Jewi", last_physical_day)
  lm["Kule"].capacity = d.getMaxFromData("Kule", last_physical_day)
  lm["Kakuma"].capacity = d.getMaxFromData("Kakuma", last_physical_day)
  lm["Khartoum"].capacity = d.getMaxFromData("Khartoum", last_physical_day)
  lm["West_Kordofan"].capacity = d.getMaxFromData("West_Kordofan", last_physical_day)
  lm["Adjumani"].capacity = d.getMaxFromData("Adjumani", last_physical_day)
  lm["Rhino"].capacity = d.getMaxFromData("Rhino", last_physical_day)
  lm["Kiryandongo"].capacity = d.getMaxFromData("Kiryandongo", last_physical_day)

  output_header_string = "Day,"

  camp_locations      = ["Tierkidi","Pugnido","Jewi","Kule","Kakuma","Khartoum","West_Kordofan","Adjumani","Rhino","Kiryandongo"]
  #TODO: Add Camps from CSV based on their location type.

  for l in camp_locations:
    #AddInitialRefugees(e,d,lm[l])
    output_header_string += "%s sim,%s data,%s error," % (lm[l].name, lm[l].name, lm[l].name)

  output_header_string += "Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,refugees in camps (simulation),refugee_debt"

  print(output_header_string)

  # Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.

  for t in range(0,end_time):

    ig.AddNewConflictZones(e,t)

    # Determine number of new refugees to insert into the system.
    new_refs = d.get_daily_difference(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_daily_difference(t, FullInterpolation=True)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    # Insert refugee agents
    e.add_agents_to_conflict_zones(new_refs)

    e.refresh_conflict_weights()

    t_data = t

    e.enact_border_closures(t)
    e.evolve()

    # Calculation of error terms
    errors = []
    abs_errors = []
    loc_data = []

    camps = []
    for i in camp_locations:
      camps += [lm[i]]
      loc_data += [d.get_field(i, t)]

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
      output += ",0,0,0,0,0,0"
      #output_string += ",0"


    print(output)

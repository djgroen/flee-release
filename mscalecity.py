from flee import pflee #parallel implementation
from flee import coupling #coupling interface for multiscale models
from datamanager import handle_refugee_data
from datamanager import DataTable #DataTable.subtract_dates()
from flee import InputGeography
import numpy as np
import outputanalysis.analysis as a
import sys
import analyze_graph

def AddInitialRefugees(e, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = 10000
  for i in range(0, num_refugees):
    e.addAgent(location=loc)

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2010-01-01")


if __name__ == "__main__":

  end_time = 10
  last_physical_day = 10
  submodel_id = 0

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      submodel_id = int(sys.argv[1])
      #duration = pflee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      #if duration>0:
      #  end_time = duration
      #  last_physical_day = end_time

  e = pflee.Ecosystem()
  c = coupling.CouplingInterface(e)
  c.setCouplingFilenames("in","out")
  if(submodel_id > 0):
    c.setCouplingFilenames("out","in")

  ig = InputGeography.InputGeography()

  ig.ReadLocationsFromCSV("examples/testmscale/locations-%s.csv" % submodel_id)

  ig.ReadLinksFromCSV("examples/testmscale/routes-%s.csv" % submodel_id)

  ig.ReadClosuresFromCSV("examples/testmscale/closures-%s.csv" % submodel_id)

  e,lm = ig.StoreInputGeographyInEcosystem(e)

  #DEBUG: print graph and show it on an image.
  vertices, edges = e.export_graph()
  #analyze_graph.print_graph_nx(vertices, edges, print_dist=True)
  #sys.exit()


  #print("Network data loaded")

  #d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="test_data/test_input_csv/refugee_data", start_date="2010-01-01", data_layout="data_layout.csv")

  output_header_string = "Day,"

  coupled_locations      = ["N","E","S","W"]
  camp_locations = list(lm.keys())

  #print(camp_locations)
  #camp_locations      = ["N","E","S","W"]
  #if(submodel_id > 0):
  #  camp_locations = ["A","B"]
  #TODO: Add Camps from CSV based on their location type.

  if submodel_id == 0:
    AddInitialRefugees(e,lm["A"])

  for l in coupled_locations:
    c.addCoupledLocation(lm[l], l)

  for l in camp_locations:
    output_header_string += "%s sim," % (lm[l].name)

  if e.getRankN(0):
    output_header_string += "num agents,num agents in camps"
    print(output_header_string)

  # Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.

  for t in range(0,end_time):

    #if t>0:
    ig.AddNewConflictZones(e,t)

    # Determine number of new refugees to insert into the system.
    new_refs = 0
    if submodel_id == 0:
      new_refs = 0
    refugees_raw += new_refs

    #Insert refugee agents
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

    e.refresh_conflict_weights()
    t_data = t

    #e.enact_border_closures(t)
    e.evolve()

    #Calculation of error terms
    errors = []
    abs_errors = []

    camps = []
    for i in camp_locations:
      camps += [lm[i]]

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for camp in camps:
      refugees_in_camps_sim += camp.numAgents

    if e.getRankN(t):
      output = "%s" % t

      for i in range(0,len(camp_locations)):
        output += ",%s" % (lm[camp_locations[i]].numAgents)

      if refugees_raw>0:
        output += ",%s,%s" % (e.numAgents(), refugees_in_camps_sim)
      else:
        output += ",0,0"

      print(output)

    #exchange data with other code.
    c.Couple(t)

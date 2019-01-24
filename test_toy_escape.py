import flee.flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  flee.SimulationSettings.SimulationSettings.MinMoveSpeed=5000.0
  flee.SimulationSettings.SimulationSettings.MaxMoveSpeed=5000.0

  end_time = 10
  e = flee.Ecosystem()

  l1 = e.addLocation("A", movechance=0.3)

  l2 = e.addLocation("B", movechance=0.0)
  l3 = e.addLocation("C", movechance=0.0)
  l4 = e.addLocation("D", movechance=0.0)

  e.linkUp("A","B","834.0")
  e.linkUp("A","C","1368.0")
  e.linkUp("A","D","536.0")

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="test_data", start_date="2010-01-01", data_layout="data_layout.csv")

  for t in range(0,end_time):
    new_refs = d.get_new_refugees(t)

    # Insert refugee agents
    for i in range(0, new_refs):
      e.addAgent(location=l1)

    # Propagate the model by one time step.
    e.evolve()

    print(t, l1.numAgents+l2.numAgents+l3.numAgents+l4.numAgents, l1.numAgents, l2.numAgents, l3.numAgents, l4.numAgents)


  assert t==9
  assert l1.numAgents+l2.numAgents+l3.numAgents+l4.numAgents==635 # This includes refugee counts from Fassala as well
  #79 746 24601 14784 38188

  print("Test successful!")

  """
    l2_data = d.get_field("Mauritania", t) - d.get_field("Mauritania", 0)
    l3_data = d.get_field("Niger", t) - d.get_field("Niger", 0)
    l4_data = d.get_field("Burkina Faso", t) - d.get_field("Burkina Faso", 0)

    errors = [a.rel_error(l2.numAgents,l2_data), a.rel_error(l3.numAgents,l3_data), a.rel_error(l4.numAgents,l4_data)]

    print "Kiffa: ", l2.numAgents, ", data: ", l2_data, ", error: ", errors[0]
    print "Niamey: ", l3.numAgents, ", data: ", l3_data, ", error: ", errors[1]
    print "Bobo-Dioulasso: ", l4.numAgents,", data: ", l4_data, ", error: ", errors[2]
    print "Cumulative error: ", np.sum(errors), ", Squared error: ", np.sqrt(np.sum(np.power(errors,2)))

  if np.abs(np.sum(errors) - 0.495521376979) > 0.1:
    print "TEST FAILED."
  if np.sqrt(np.sum(np.power(errors,2))) > 0.33+0.03:
    print "TEST FAILED."
  else:
    print "TEST SUCCESSFUL."
  """

import flee.flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a
import sys

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  flee.SimulationSettings.MinMoveSpeed=5000.0
  flee.SimulationSettings.MaxMoveSpeed=5000.0
  flee.SimulationSettings.MaxWalkSpeed=5000.0

  if(len(sys.argv)>1):
    flee.SimulationSettings.AwarenessLevel = int(sys.argv[1])

  end_time = 10
  e = flee.Ecosystem()

  l1 = e.addLocation("A", movechance=0.3)

  l2 = e.addLocation("B", movechance=0.3)
  l3 = e.addLocation("C", movechance=0.3)
  l4 = e.addLocation("D", movechance=0.3)
  l5 = e.addLocation("C2", movechance=0.3)
  l6 = e.addLocation("D2", movechance=0.3)
  l7 = e.addLocation("D3", movechance="camp")

  e.linkUp("A","B","834.0")
  e.linkUp("A","C","834.0")
  e.linkUp("A","D","834.0")
  e.linkUp("C","C2","834.0")
  e.linkUp("C","D2","834.0")
  e.linkUp("D","D2","834.0")
  e.linkUp("D2","D3","834.0")
  e.linkUp("C2","D3","834.0")

  e.addAgent(location=l1)

  e.agents[0].selectRouteRuleset2(debug=True)

  #for t in range(0,end_time):

  # Propagate the model by one time step.
  #  e.evolve()

  print("Test successful!")


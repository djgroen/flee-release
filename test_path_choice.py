import flee.flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  flee.SimulationSettings.MinMoveSpeed=5000.0
  flee.SimulationSettings.MaxMoveSpeed=5000.0
  flee.SimulationSettings.MaxWalkSpeed=5000.0

  e = flee.Ecosystem()

  l1 = e.addLocation("A", movechance=1.0)

  l2 = e.addLocation("B", movechance=1.0)
  l3 = e.addLocation("C1", movechance=1.0)
  l4 = e.addLocation("C2", movechance=1.0)
  l5 = e.addLocation("D1", movechance=1.0)
  l6 = e.addLocation("D2", movechance=1.0)
  l7 = e.addLocation("D3", movechance=1.0)

  e.linkUp("A","B","10.0")
  e.linkUp("A","C1","10.0")
  e.linkUp("A","D1","10.0")
  e.linkUp("C1","C2","10.0")
  e.linkUp("D1","D2","10.0")
  e.linkUp("D2","D3","10.0")

  e.addAgent(location=l1)


  print("Test successful!")


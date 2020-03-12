import flee.flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  flee.SimulationSettings.MinMoveSpeed=10.0
  flee.SimulationSettings.MaxMoveSpeed=10.0

  end_time = 100
  e = flee.Ecosystem()

  l1 = e.addLocation("A", movechance=1.0)
  l2 = e.addLocation("B", movechance=0.0)

  e.linkUp("A","B","5.0")


  for t in range(0,end_time):
    # Insert refugee agents
    e.addAgent(location=l1)

    # Propagate the model by one time step.
    e.evolve()

    if t==2:
      assert e.close_location("B")

    print(t, l1.numAgents, l2.numAgents)
    e.printComplete()

  assert t==99
  assert l2.numAgents==3 # Location is closed after 3 steps, refugees underway will still arrive but others are blocked.
  assert l1.numAgents==97

  print("Test successful!")


import flee.micro_flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  flee.SimulationSettings.MaxMoveSpeed=35.0
  flee.SimulationSettings.MaxWalkSpeed=3.5
  flee.SimulationSettings.MaxCrossingSpeed=2.0

  end_time = 10
  e = flee.Ecosystem()

  l1 = e.addLocation("A", movechance=0.3)

  l2 = e.addLocation("B", movechance=0.3)
  l3 = e.addLocation("C", movechance=0.0)
  l4 = e.addLocation("D", movechance=0.0)

  e.linkUp("A","B","20.0","drive")
  e.linkUp("A","C","10.0","drive")
  e.linkUp("B","C","10.0","crossing")
  e.linkUp("A","D","10.0","walk")
  e.linkUp("C","D","5.0","walk")

  new_refs = 10

  # Insert refugee agents
  for i in range(0, new_refs):
    e.addAgent(location=l1)

  for t in range(0,end_time):

    # Propagate the model by one time step.
    e.evolve()

    print("Our agents are at", e.agents[0].location.name)

    print(t, l1.numAgents+l2.numAgents+l3.numAgents+l4.numAgents, l1.numAgents, l2.numAgents, l3.numAgents, l4.numAgents)


  assert t==9
  assert l1.numAgents+l2.numAgents+l3.numAgents+l4.numAgents==10 

  print("Test successful!")


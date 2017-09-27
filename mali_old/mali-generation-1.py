import flee
import handle_refugee_data
import numpy as np
import analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Simulating Mali.")

  end_time = 80
  e = flee.Ecosystem()

  l1 = e.addLocation("Bamako", movechance=0.3)

# Mauritania

# Burkina Faso

# Niger
  l2 = e.addLocation("Kiffa", movechance=0.0)
  l3 = e.addLocation("Niamey", movechance=0.0)
  l4 = e.addLocation("Bobo-Dioulasso", movechance=0.0)

  e.linkUp("Bamako","Kiffa","834.0")
  e.linkUp("Bamako","Niamey","1368.0")
  e.linkUp("Bamako","Bobo-Dioulasso","536.0")

  d = handle_refugee_data.DataTable("source-data-unhcr.txt", csvformat="mali-pdf")

  for t in range(0,end_time):
    new_refs = d.get_new_refugees(t)
    for i in range(0, new_refs):
      e.addAgent(location=l1)
    e.evolve()
#    e.printInfo()
    print t
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

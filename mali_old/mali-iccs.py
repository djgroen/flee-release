import flee
import handle_refugee_data
import numpy as np
import analysis as a
import sys

def linkBF(e):
  # bing based
  e.linkUp("Douentza","Mentao","487.0")
  e.linkUp("Mopti","Mentao","360.0")
  e.linkUp("Mopti","Bobo-Dioulasso","462.0")
  e.linkUp("Mentao","Bobo-Dioulasso","475.0")

def linkNiger(e):
  # bing based
  e.linkUp("Menaka","Abala","172.0")
  #e.linkUp("Gao","Mangaize","455.0")
  e.linkUp("Menaka","Mangaize","305.0")
  #e.linkUp("Gao","Niamey","444.0")
  #e.linkUp("Menaka","Niamey","559.0")
  e.linkUp("Gao","Tabareybarey","245.0")
  e.linkUp("Menaka","Tabareybarey","361.0")

  # All distances here are Bing-based.
  e.linkUp("Abala","Mangaize","256.0")
  e.linkUp("Abala","Niamey","253.0")
  e.linkUp("Abala","Tabareybarey","412.0")
  e.linkUp("Mangaize","Niamey","159.0")
  e.linkUp("Mangaize","Tabareybarey","217.0")
  e.linkUp("Niamey","Tabareybarey","205.0")


def AddInitialRefugees(e, d, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = int(d.get_field(loc.name, 0))
  for i in range(0, num_refugees):
    e.addAgent(location=loc)


if __name__ == "__main__":

  if len(sys.argv)>1:
    end_time = int(sys.argv[1])
  else:
    end_time = 61

  e = flee.Ecosystem()

# Distances are estimated using Bing Maps.

# Mali
  
  o1 = e.addLocation("Kidal", movechance=0.5)
  # pop. 25,617. GPS 18.444305 1.401523
  o2 = e.addLocation("Gao", movechance=0.5)
  # pop. 86,633. GPS 16.270910 -0.040210
  o3 = e.addLocation("Timbuktu", movechance=0.5)
  # pop. 54,453. GPS 16.780260 -3.001590
  o4 = e.addLocation("Mopti", movechance=0.5)
  # pop. 108,456 (2009 census)
  o5 = e.addLocation("Douentza", movechance=0.5)
  # pop. 28,005 (2009 census), fell on 5th of April 2012.
  o6 = e.addLocation("Konna", movechance=0.5)
  # pop. 36,767 (2009 census), captured in January 2013 by the Islamists.
  o6 = e.addLocation("Menaka", movechance=1.0)
  # pop. 20,702 (2009 census), captured in January 2012 by the Islamists.
  o7 = e.addLocation("Niafounke", movechance=1.0)
  # pop. negligible. Added because it's a junction point, move chance set to 1.0 for that reason.
  o8 = e.addLocation("Bourem", movechance=0.5)
  # pop. 27,486. GPS 16.968122, -0.358435. No information about capture yet, but it's a sizeable town at a junction point.

  # bing based
  e.linkUp("Kidal","Bourem", "308.0") #964.0
  e.linkUp("Gao","Bourem","97.0") #612
  e.linkUp("Timbuktu","Bourem","314.0")

  e.linkUp("Timbuktu", "Konna","303.0") #Mopti is literally on the way to Bobo-Dioulasso.
  e.linkUp("Gao", "Douentza","397.0") #Mopti is literally on the way to Bobo-Dioulasso.
  e.linkUp("Douentza","Konna","121.0") #Douentza is on the road between Gao and Mopti.
  e.linkUp("Konna","Mopti","70.0") #Douentza is on the road between Gao and Mopti.

  e.linkUp("Gao","Menaka","314.0")

  e.linkUp("Timbuktu","Niafounke","162.0")
  e.linkUp("Niafounke","Konna","153.0")

# Mauritania

  m1 = e.addLocation("Mbera", movechance=0.001, capacity=103731, foreign=True)
  # GPS 15.639012,-5.751422
  m2 = e.addLocation("Fassala", movechance=0.08, foreign=True)

  # bing based
  e.linkUp("Niafounke","Fassala","241.0")
  e.linkUp("Fassala","Mbera","25.0", forced_redirection=True)

# Burkina Faso

  b1 = e.addLocation("Mentao", movechance=0.001, capacity=10038, foreign=True)
  # GPS 13.999700,-1.680371
  b2 = e.addLocation("Bobo-Dioulasso", movechance=0.001, capacity=1926, foreign=True)
  # GPS 11.178103,-4.291773

  # No linking up yet, as BF border was shut prior to March 21st 2012.

# Niger
  n1 = e.addLocation("Abala", movechance=0.001, capacity=18573, foreign=True)
  # GPS 14.927683 3.433727
  n2 = e.addLocation("Mangaize", movechance=0.001, capacity=4356, foreign=True)
  # GPS 14.684030 1.882720
  n3 = e.addLocation("Niamey", movechance=0.001, capacity=6327, foreign=True)

  n4 = e.addLocation("Tabareybarey", movechance=0.001, capacity=9189, foreign=True)
  # GPS 14.754761 0.944773

  d = handle_refugee_data.DataTable(csvformat="generic", data_directory="mali2012/")

  print("Day,Mbera sim,Mbera data,Mbera error,Fassala sim,Fassala data,Fassala error,Mentao sim,Mentao data,Mentao error,Bobo-Dioulasso sim,Bobo-Dioulasso data,Bobo-Dioulasso error,Abala sim,Abala data,Abala error,Mangaize sim,Mangaize data,Mangaize error,Niamey sim,Niamey data,Niamey error,Tabareybarey sim,Tabareybarey data,Tabareybarey error,Total error,refugees in camps (UNHCR),refugees in camps (simulation),raw UNHCR refugee count")

  # Kidal has fallen. All refugees want to leave this place.
  o1.movechance = 1.0

  # Set up a mechanism to incorporate temporary decreases in refugees 
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.
 
  # Add initial refugees to the destinations. 
  AddInitialRefugees(e,d,m1)
  AddInitialRefugees(e,d,m2)
  AddInitialRefugees(e,d,b1)
  AddInitialRefugees(e,d,b2)
  AddInitialRefugees(e,d,n1)
  AddInitialRefugees(e,d,n2)
  AddInitialRefugees(e,d,n3)
  AddInitialRefugees(e,d,n4)

  conflict_zones = [o1]
  conflict_weights = np.array([68000])


  for t in range(0,end_time):

    # Close/open borders here.
    if t==20: #On the 19th of March, Fassala closes altogether, and instead functions as a forward to Mbera (see PDF report 1 and 2).
      m2.movechance = 1.0
    if t==22: #On the 21st of March, Burkina Faso opens its borders (see PDF report 3).
      linkBF(e)   
    if t==31: #Starting from April, refugees appear to enter Niger again (on foot, report 4).
      linkNiger(e)


    new_refs = d.get_new_refugees(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_new_refugees(t, FullInterpolation=False)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0

    if t==31: #Kidal has fallen, but Gao and Timbuktu are still controlled by Mali
      o2.movechance = 1.0 # Refugees now want to leave Gao.
      o3.movechance = 1.0 # Refugees now want to leave Timbuktu.
    
      # This is used to append two locations to the list of conflict zones (a Python List).
      conflict_zones += [o2,o3]
      # And this is used to append two weights to the weights array (a NumPy array).
      conflict_weights = np.append(conflict_weights, [544000,682000])      
 
    # Here we use the random choice to make a weighted choice between the 1-3 source locations.
    for i in range(0, new_refs):
      e.addAgent(np.random.choice(conflict_zones, p=conflict_weights/sum(conflict_weights)))

    e.evolve()

    # Basic output
    # e.printInfo()

    
    # Validation / data comparison
    m1_data = d.get_field("Mbera", t) #- d.get_field("Mbera", 0)
    m2_data = d.get_field("Fassala", t) #- d.get_field("Mbera", 0)
    b1_data = d.get_field("Mentao", t) #- d.get_field("Mentao", 0)
    b2_data = d.get_field("Bobo-Dioulasso", t) #- d.get_field("Bobo-Dioulasso", 0)
    n1_data = d.get_field("Abala", t) #- d.get_field("Abala", 0)
    n2_data = d.get_field("Mangaize", t) #- d.get_field("Mangaize", 0)
    n3_data = d.get_field("Niamey", t) #- d.get_field("Niamey", 0)
    n4_data = d.get_field("Tabareybarey", t) #- d.get_field("Tabareybarey", 0)

    errors = [a.rel_error(m1.numAgents,m1_data), a.rel_error(m2.numAgents,m2_data), a.rel_error(b1.numAgents,b1_data), a.rel_error(b2.numAgents,b2_data), a.rel_error(n1.numAgents,n1_data), a.rel_error(n2.numAgents,n2_data), a.rel_error(n3.numAgents,n3_data), a.rel_error(n4.numAgents,n4_data)]
    abs_errors = [a.abs_error(m1.numAgents,m1_data), a.abs_error(m2.numAgents,m2_data), a.abs_error(b1.numAgents,b1_data), a.abs_error(b2.numAgents,b2_data), a.abs_error(n1.numAgents,n1_data), a.abs_error(n2.numAgents,n2_data), a.abs_error(n3.numAgents,n3_data), a.abs_error(n4.numAgents,n4_data)]
    locations = [m1,m2,b1,b2,n1,n2,n3,n4]
    loc_data = [m1_data,m2_data,b1_data,b2_data,n1_data,n2_data,n3_data,n4_data]
   

    #print "Mbera: ", m1.numAgents, ", data: ", m1_data, ", error: ", errors[0]
    #print "Mentao: ", b1.numAgents, ", data: ", b1_data, ", error: ", errors[1]
    #print "Bobo-Dioulasso: ", b2.numAgents,", data: ", b2_data, ", error: ", errors[2]
    #print "Abala: ", n1.numAgents,", data: ", n1_data, ", error: ", errors[3]
    #print "Mengaize: ", n2.numAgents,", data: ", n2_data, ", error: ", errors[4]
    #if e.numAgents()>0:
    #  print "Total error: ", float(np.sum(abs_errors))/float(e.numAgents())

    output = "%s" % (t)
    for i in range(0,len(errors)):
      output += ",%s,%s,%s" % (locations[i].numAgents, loc_data[i], errors[i])

    if e.numAgents()>0:
      output += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(sum(loc_data)), int(sum(loc_data)), e.numAgents(), refugees_raw)
    else:
      output += ",0"

    print(output)

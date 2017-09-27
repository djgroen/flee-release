import flee
import handle_refugee_data
import numpy as np
import analysis as a
import sys

def linkBF(e):
  # bing based
  e.linkUp("Kidal","Mentao","1285.0")
  e.linkUp("Gao","Mentao","883.0")
  e.linkUp("Timbuktu","Mentao","733.0")

  # birds flight
  #e.linkUp("Kidal","Mentao","592.0")
  #e.linkUp("Gao","Mentao","307.0")
  #e.linkUp("Timbuktu","Mentao","339.0")

  # bing based
  e.linkUp("Kidal","Bobo-Dioulasso","1430.0")
  e.linkUp("Gao","Bobo-Dioulasso","1029.0")
  e.linkUp("Timbuktu","Bobo-Dioulasso","830.0")

  # birds flight
  #e.linkUp("Kidal","Bobo-Dioulasso","1011.0")
  #e.linkUp("Gao","Bobo-Dioulasso","727.0")
  #e.linkUp("Timbuktu","Bobo-Dioulasso","635.0")

  e.linkUp("Mentao","Bobo-Dioulasso","475.0")

def linkNiger(e):
  # bing based
  e.linkUp("Kidal","Abala","1099.0")
  e.linkUp("Gao","Abala","696.0")
  e.linkUp("Timbuktu","Abala","1108.0")

  # birds flight
  #e.linkUp("Kidal","Abala","445.0")
  #e.linkUp("Gao","Abala","401.0")
  #e.linkUp("Timbuktu","Abala","719.0")

  # bing based
  e.linkUp("Kidal","Mangaize","858.0")
  e.linkUp("Gao","Mangaize","455.0")
  e.linkUp("Timbuktu","Mangaize","867.0")

  # birds flight
  #e.linkUp("Kidal","Mangaize","419.0")
  #e.linkUp("Gao","Mangaize","271.0")
  #e.linkUp("Timbuktu","Mangaize","572.0")

  e.linkUp("Abala","Mangaize","256.0")


if __name__ == "__main__":

  if len(sys.argv)>1:
    end_time = int(sys.argv[1])
  else:
    end_time = 61

  e = flee.Ecosystem()

# Distances are estimated using Bing Maps.

# Mali
  
  o1 = e.addLocation("Kidal", movechance=0.3)
  # GPS 18.444305 1.401523
  o2 = e.addLocation("Gao", movechance=0.3)
  # GPS 16.270910 -0.040210
  o3 = e.addLocation("Timbuktu", movechance=0.3)
  # GPS 16.780260 -3.001590

  # bing based
  e.linkUp("Kidal","Gao","402.0") #354 in Google, 
  e.linkUp("Kidal","Timbuktu", "622.0") #964.0
  e.linkUp("Gao","Timbuktu","411.0") #612

  # birds flight
  #e.linkUp("Kidal","Gao","285.0")  
  #e.linkUp("Kidal","Timbuktu", "502.0") 
  #e.linkUp("Gao","Timbuktu","321.0") 

# Mauritania

  m1 = e.addLocation("Mbera", movechance=0.001)
  # GPS 15.639012 -5.751422

  # bing based
  e.linkUp("Kidal","Mbera","1049.0")
  e.linkUp("Gao","Mbera","839.0")
  e.linkUp("Timbuktu","Mbera","428.0")
  
  # birds flight
  #e.linkUp("Kidal","Mbera","822.0")
  #e.linkUp("Gao","Mbera","615.0")
  #e.linkUp("Timbuktu","Mbera","320.0")

# Burkina Faso

  b1 = e.addLocation("Mentao", movechance=0.001)
  # GPS 13.999700 -1.680371
  b2 = e.addLocation("Bobo-Dioulasso", movechance=0.001)
  # GPS 11.178103 -4.291773

  # No linking up yet, as BF border was shut prior to March 21st 2012.

# Niger
  n1 = e.addLocation("Abala", movechance=0.001)
  # GPS 14.927683 3.433727
  n2 = e.addLocation("Mangaize", movechance=0.0001)
  # GPS 14.684030 1.882720
  n3 = e.addLocation("Niamey", movechance=0.001)

  n4 = e.addLocation("Tabareybarey", movechance=0.001)

  d = handle_refugee_data.DataTable("mali2012/refugees.csv", csvformat="mali-portal")

  print "Day,Mbera sim,Mbera data,Mbera error,Mentao sim,Mentao data,Mentao error,Bobo-Dioulasso sim,Bobo-Dioulasso data,Bobo-Dioulasso error,Abala sim,Abala data,Abala error,Mangaize sim,Mangaize data,Mangaize error,Total error,numAgents,numAgents sim,raw refugee total"

  # Kidal has fallen. All refugees want to leave this place.
  o1.movechance = 1.0

  # Set up a mechanism to incorporate temporary decreases in refugees 
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only.
 
  for t in xrange(0,end_time):

    # Close/open borders here.
    if(t==22): #On the 21st of March, Burkina Faso opens its borders (see PDF report 3).
      linkBF(e)
    if(t==31): #Starting from April, refugees appear to enter Niger again (on foot, report 4).
      linkNiger(e)


    new_refs = d.get_new_refugees(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_new_refugees(t, FullInterpolation=False)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0

    for i in xrange(0, new_refs):

      if(t<31): #Kidal has fallen, but Gao and Timbuktu are still controlled by Mali
        e.addAgent(location=o1)

      else: #All three cities have fallen
        o2.movechance = 1.0 # Refugees now want to leave Gao.
        o3.movechance = 1.0 # Refugees now want to leave Timbuktu.

        # Population numbers source: UNHCR (2009 Mali census)
        pop_kidal_region = 68000
        pop_gao_region = 544000
        pop_timbuktu_region = 682000
        pop_total = pop_kidal_region + pop_gao_region + pop_timbuktu_region
        dice_roll = np.random.randint(pop_total)

        if dice_roll < pop_kidal_region:
          e.addAgent(location=o1) #Add refugee to Kidal
        elif dice_roll < pop_kidal_region + pop_gao_region:
          e.addAgent(location=o2) #Add refugee to Gao
        else:
          e.addAgent(location=o3) #Add refugee to Timbuktu

    e.evolve()

    # Basic output
    # e.printInfo()

    # Validation / data comparison

    m1_data = d.get_field("Mbera", t) - d.get_field("Mbera", 0)
    b1_data = d.get_field("Mentao", t) - d.get_field("Mentao", 0)
    b2_data = d.get_field("Bobo-Dioulasso", t) - d.get_field("Bobo-Dioulasso", 0)
    n1_data = d.get_field("Abala", t) - d.get_field("Abala", 0)
    n2_data = d.get_field("Mangaize", t) - d.get_field("Mangaize", 0)

    errors = [a.rel_error(m1.numAgents,m1_data), a.rel_error(b1.numAgents,b1_data), a.rel_error(b2.numAgents,b2_data), a.rel_error(n1.numAgents,n1_data), a.rel_error(n2.numAgents,n2_data)]
    abs_errors = [a.abs_error(m1.numAgents,m1_data), a.abs_error(b1.numAgents,b1_data), a.abs_error(b2.numAgents,b2_data), a.abs_error(n1.numAgents,n1_data), a.abs_error(n2.numAgents,n2_data)]
    locations = [m1,b1,b2,n1,n2]
    loc_data = [m1_data,b1_data,b2_data,n1_data,n2_data]
   

    #print "Mbera: ", m1.numAgents, ", data: ", m1_data, ", error: ", errors[0]
    #print "Mentao: ", b1.numAgents, ", data: ", b1_data, ", error: ", errors[1]
    #print "Bobo-Dioulasso: ", b2.numAgents,", data: ", b2_data, ", error: ", errors[2]
    #print "Abala: ", n1.numAgents,", data: ", n1_data, ", error: ", errors[3]
    #print "Mengaize: ", n2.numAgents,", data: ", n2_data, ", error: ", errors[4]
    #if e.numAgents()>0:
    #  print "Total error: ", float(np.sum(abs_errors))/float(e.numAgents())

    output = "%s" % (t)
    for i in xrange(0,len(errors)):
      output += ",%s,%s,%s" % (locations[i].numAgents, loc_data[i], errors[i])

    if e.numAgents()>0:
      output += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(sum(loc_data)), int(sum(loc_data)), e.numAgents(), refugees_raw)
    else:
      output += ",0"

    print output

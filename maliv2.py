from flee import flee
from datamanager import handle_refugee_data
from datamanager import DataTable #DataTable.subtract_dates()
import numpy as np
import outputanalysis.analysis as a
import sys

def linkBF(e):
  # bing based
  e.linkUp("Douentza","Mentao","487.0")
  e.linkUp("Mopti","Mentao","360.0")
  e.linkUp("Mopti","Bobo-Dioulasso","462.0")
  e.linkUp("Segou","Bobo-Dioulasso","376.3")
  e.linkUp("Mentao","Bobo-Dioulasso","475.0")

def linkNiger(e):
  # bing based
  e.linkUp("Menaka","Abala","172.0")
  e.linkUp("Menaka","Mangaize","305.0")
  e.linkUp("Ansongo","Tabareybarey","148.4")
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
  num_refugees = int(d.get_field(loc.name, 0, FullInterpolation=True))
  for i in range(0, num_refugees):
    e.addAgent(location=loc)

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2012-02-29")


if __name__ == "__main__":

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 300
      last_physical_day = 300
      duration = flee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time
  else:
    end_time = 300
    last_physical_day = 300

  e = flee.Ecosystem()

  # Refugees reduce population counts.
  #flee.SimulationSettings.TakeRefugeesFromPopulation = True

  # Distances are estimated using Bing Maps.

  # Mali

  lm = {}

  lm["Kidal"] = e.addLocation("Kidal", movechance="default", pop=25617)
  # pop. 25,617. GPS 18.444305 1.401523
  lm["Gao"] = e.addLocation("Gao", movechance="default", pop=86633)
  # pop. 86,633. GPS 16.270910 -0.040210
  lm["Timbuktu"] = e.addLocation("Timbuktu", movechance="default", pop=54453)
  # pop. 54,453. GPS 16.780260 -3.001590
  lm["Mopti"] = e.addLocation("Mopti", movechance="default", pop=148456) #108456 from Mopti + 40000 from Sevare, which is 10km southeast to Mopti.
  # pop. 108,456 (2009 census)
  lm["Douentza"] = e.addLocation("Douentza", movechance="default", pop=28005)
  # pop. 28,005 (2009 census), fell on 5th of April 2012.
  lm["Konna"] = e.addLocation("Konna", movechance="default", pop=36767)
  # pop. 36,767 (2009 census), captured in January 2013 by the Islamists.
  lm["Menaka"] = e.addLocation("Menaka", movechance="conflict", pop=20702)
  # pop. 20,702 (2009 census), captured in January 2012 by the Islamists.
  lm["Niafounke"] = e.addLocation("Niafounke", movechance="conflict", pop=1000)
  # pop. negligible. Added because it's a junction point, move chance set to 1.0 for that reason.
  lm["Bourem"] = e.addLocation("Bourem", movechance="default", pop=27486)
  # pop. 27,486. GPS 16.968122, -0.358435. No information about capture yet, but it's a sizeable town at a junction point.
  lm["Bamako"] = e.addLocation("Bamako", movechance="default", pop=1809106)
  # pop. 1,809,106 capital subject to coup d'etat between March 21st and April 8th 2012.
  lm["Tenenkou"] = e.addLocation("Tenenkou", movechance="default", pop=11310)
  # pop. 11310. First Battle on 02-03-2012, 14.5004532,-4.8748448.
  lm["Segou"] = e.addLocation("Segou", movechance="default", pop=130690)

  lm["Ansongo"] = e.addLocation("Ansongo", movechance="default", pop=32709)
  # pop. 32709
  lm["Lere"] = e.addLocation("Lere", movechance="default", pop=16072)
  # pop. 16,072.
  lm["Dire"] = e.addLocation("Dire", movechance="default", pop=22365)
  # pop. 22,365.
  lm["Goundam"] = e.addLocation("Goundam", movechance="default", pop=16253)
  # pop. 16,253.


  """
  Town merges in Mali, as they are <= 10 km away:
  ACLED towns -> town in simulation
  Kati, Kambila, Badalabougo -> Bamako
  Sevare -> Mopti
  """

  # bing based
  e.linkUp("Kidal","Bourem", "308.0")
  e.linkUp("Gao","Bourem","97.0")
  e.linkUp("Timbuktu","Bourem","314.0")

  e.linkUp("Timbuktu", "Konna","303.0") #Mopti is literally on the way to Bobo-Dioulasso.
  e.linkUp("Gao", "Douentza","397.0") #Mopti is literally on the way to Bobo-Dioulasso.
  e.linkUp("Douentza","Konna","121.0") #Douentza is on the road between Gao and Mopti.
  e.linkUp("Konna","Mopti","70.0") #Konna is on the road between Gao and Mopti.
  e.linkUp("Mopti","Segou","401.3")

  e.linkUp("Ansongo","Menaka","190.7")
  e.linkUp("Gao","Ansongo","99.6")

  e.linkUp("Dire","Goundam","42.2")
  e.linkUp("Goundam","Timbuktu","85.3")
  e.linkUp("Goundam","Niafounke","77.5")
  e.linkUp("Niafounke","Konna","153.0")
  e.linkUp("Niafounke", "Lere", "139.8")

  e.linkUp("Tenenkou","Niafounke","308.1")
  e.linkUp("Tenenkou","Lere","294.5")
  e.linkUp("Tenenkou","Segou","227.5")
  e.linkUp("Segou","Bamako","239.8")


# Mauritania

  m1 = e.addLocation("Mbera", movechance="camp", capacity=103731, foreign=True)
  # GPS 15.639012,-5.751422
  m2 = e.addLocation("Fassala", movechance=0.08, foreign=True)

  # bing based
  e.linkUp("Lere","Fassala","98.1")
  e.linkUp("Fassala","Mbera","25.0", forced_redirection=True)

# Burkina Faso

  b1 = e.addLocation("Mentao", movechance="camp", capacity=10038, foreign=True)
  # GPS 13.999700,-1.680371
  b2 = e.addLocation("Bobo-Dioulasso", movechance="camp", capacity=1926, foreign=True)
  # GPS 11.178103,-4.291773

  # No linking up yet, as BF border was shut prior to March 21st 2012.

# Niger
  n1 = e.addLocation("Abala", movechance="camp", capacity=18573, foreign=True)
  # GPS 14.927683 3.433727
  n2 = e.addLocation("Mangaize", movechance="camp", capacity=4356, foreign=True)
  # GPS 14.684030 1.882720
  n3 = e.addLocation("Niamey", movechance="camp", capacity=6327, foreign=True)

  n4 = e.addLocation("Tabareybarey", movechance="camp", capacity=9189, foreign=True)
  # GPS 14.754761 0.944773

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="source_data/mali2012/")

  # Correcting for overestimations due to inaccurate level 1 registrations in five of the camps.
  # These errors led to a perceived large drop in refugee population in all of these camps.
  # We correct by linearly scaling the values down to make the last level 1 registration match the first level 2 registration value.
  # To our knowledge, all level 2 registration procedures were put in place by the end of 2012.
  d.correctLevel1Registrations("Mbera","2012-12-31")
  m1.capacity = d.getMaxFromData("Mbera", last_physical_day)
  d.correctLevel1Registrations("Mentao","2012-10-03")
  b1.capacity = d.getMaxFromData("Mentao", last_physical_day)
  d.correctLevel1Registrations("Abala","2012-12-21")
  n1.capacity = d.getMaxFromData("Abala", last_physical_day)
  d.correctLevel1Registrations("Mangaize","2012-12-21")
  n2.capacity = d.getMaxFromData("Mangaize", last_physical_day)
  d.correctLevel1Registrations("Tabareybarey","2012-12-21")
  n4.capacity = d.getMaxFromData("Tabareybarey", last_physical_day)


  print("Day,Mbera sim,Mbera data,Mbera error,Mentao sim,Mentao data,Mentao error,Bobo-Dioulasso sim,Bobo-Dioulasso data,Bobo-Dioulasso error,Abala sim,Abala data,Abala error,Mangaize sim,Mangaize data,Mangaize error,Niamey sim,Niamey data,Niamey error,Tabareybarey sim,Tabareybarey data,Tabareybarey error,Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),refugee_debt,Total error (retrofitted)")

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

  e.add_conflict_zone("Menaka")

  # Start with a refugee debt to account for the mismatch between camp aggregates and total UNHCR data.
  refugee_debt = e.numAgents()

  t_retrofitted = 0

  for t in range(0,end_time):

    e.refresh_conflict_weights()

    t_data = t

    # Close/open borders here.
    if t_data == date_to_sim_days("2012-03-19"): #On the 19th of March, Fassala closes altogether, and instead functions as a forward to Mbera (see PDF report 1 and 2).
      m2.movechance = 1.0
    if t_data == date_to_sim_days("2012-03-21"): #On the 21st of March, Burkina Faso opens its borders (see PDF report 3).
      linkBF(e)
    if t_data == date_to_sim_days("2012-04-01"): #Starting from April, refugees appear to enter Niger again (on foot, report 4).
      linkNiger(e)

    # Determine number of new refugees to insert into the system.
    new_refs = d.get_daily_difference(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_daily_difference(t, FullInterpolation=True)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    # Add conflict zones at the right time.
    if t_data == date_to_sim_days("2012-02-03"):
      e.add_conflict_zone("Kidal")

    if t_data == date_to_sim_days("2012-02-03"):
      e.add_conflict_zone("Timbuktu")

    if t_data == date_to_sim_days("2012-03-02"):
      e.add_conflict_zone("Tenenkou")

    if t_data == date_to_sim_days("2012-03-23"):
      e.add_conflict_zone("Gao")

    if t_data == date_to_sim_days("2012-08-10"):
      e.add_conflict_zone("Bamako")

    if t_data == date_to_sim_days("2012-03-30"):
      e.add_conflict_zone("Bourem")

    if t_data == date_to_sim_days("2012-09-01"):
      e.add_conflict_zone("Douentza")

    if t_data == date_to_sim_days("2012-11-28"):
      e.add_conflict_zone("Lere")

    if t_data == date_to_sim_days("2012-03-30"):
      e.add_conflict_zone("Ansongo")

    if t_data == date_to_sim_days("2012-03-13"):
      e.add_conflict_zone("Dire")


    # Here we use the random choice to make a weighted choice between the source locations.
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

    e.evolve()

    # Validation / data comparison
    camps = [m1,b1,b2,n1,n2,n3,n4]
    camp_names = ["Mbera", "Mentao", "Bobo-Dioulasso", "Abala", "Mangaize", "Niamey", "Tabareybarey"]
    # TODO: refactor camp_names using list comprehension.

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents
    t_retrofitted = d.retrofit_time_to_refugee_count(refugees_in_camps_sim, camp_names)

    # calculate error terms.
    camp_pops = []
    errors = []
    abs_errors = []
    camp_pops_retrofitted = []
    errors_retrofitted = []
    abs_errors_retrofitted = []
    for i in range(0, len(camp_names)):
      # normal 1 step = 1 day errors.
      camp_pops += [d.get_field(camp_names[i], t, FullInterpolation=True)]
      errors += [a.rel_error(camps[i].numAgents, camp_pops[-1])]
      abs_errors += [a.abs_error(camps[i].numAgents, camp_pops[-1])]

      # errors when using retrofitted time stepping.
      camp_pops_retrofitted += [d.get_field(camp_names[i], t_retrofitted, FullInterpolation=True)]
      errors_retrofitted += [a.rel_error(camps[i].numAgents, camp_pops_retrofitted[-1])]
      abs_errors_retrofitted += [a.abs_error(camps[i].numAgents, camp_pops_retrofitted[-1])]

    # Total error is calculated using float(np.sum(abs_errors))/float(refugees_raw))

    locations = camps
    loc_data = camp_pops

    #if e.numAgents()>0:
    #  print "Total error: ", float(np.sum(abs_errors))/float(e.numAgents())

    # write output (one line per time step taken.
    output = "%s" % (t)
    for i in range(0,len(locations)):
      output += ",%s,%s,%s" % (locations[i].numAgents, loc_data[i], errors[i])

    if float(sum(loc_data))>0:
      # Reminder: Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),Total error (retrofitted)
      output += ",%s,%s,%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, t_retrofitted, refugees_in_camps_sim, refugee_debt, float(np.sum(abs_errors_retrofitted))/float(refugees_raw))
    else:
      output += ",0,0,0,0,0,0,0"

    print(output)



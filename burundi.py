from flee import flee
from datamanager import handle_refugee_data
from datamanager import DataTable
import numpy as np
import outputanalysis.analysis as a
import sys

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

#Burundi Simulation


def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2015-05-01")

if __name__ == "__main__":

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 396
      last_physical_day = 396
      duration = flee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time
  else:
    end_time = 396
    last_physical_day = 396

  e = flee.Ecosystem()

  locations = []

  #Burundi
  locations.append(e.addLocation("Bujumbura", movechance="conflict", pop=497166))
  locations.append(e.addLocation("Bubanza", movechance="default"))
  locations.append(e.addLocation("Bukinanyana", movechance="default", pop=75750))
  locations.append(e.addLocation("Cibitoke", movechance="default", pop=460435))
  locations.append(e.addLocation("Isale", movechance="default"))

  locations.append(e.addLocation("Muramvya", movechance="default"))
  locations.append(e.addLocation("Kayanza", movechance="default"))
  locations.append(e.addLocation("Kabarore", movechance="default", pop=62303)) #This resides in Kayanza province in Burundi. Not to be confused with Kabarore, Rwanda.
  locations.append(e.addLocation("Mwaro", movechance="default", pop=273143))
  locations.append(e.addLocation("Rumonge", movechance="default"))

  locations.append(e.addLocation("Burambi", movechance="default", pop=57167))
  locations.append(e.addLocation("Bururi", movechance="default"))
  locations.append(e.addLocation("Rutana", movechance="default"))
  locations.append(e.addLocation("Makamba", movechance="default"))
  locations.append(e.addLocation("Gitega", movechance="default"))

  locations.append(e.addLocation("Karuzi", movechance="default"))
  locations.append(e.addLocation("Ruyigi", movechance="default"))
  locations.append(e.addLocation("Gisuru", movechance="default", pop=99461))
  locations.append(e.addLocation("Cankuzo", movechance="default"))
  locations.append(e.addLocation("Muyinga", movechance="default"))

  locations.append(e.addLocation("Kirundo", movechance="default"))
  locations.append(e.addLocation("Ngozi", movechance="default"))
  locations.append(e.addLocation("Gashoho", movechance="default"))
  locations.append(e.addLocation("Gitega-Ruyigi", movechance="default"))
  locations.append(e.addLocation("Makebuko", movechance="default"))

  locations.append(e.addLocation("Commune of Mabanda", movechance="default"))

  #Rwanda, Tanzania, Uganda and DRCongo camps
  locations.append(e.addLocation("Mahama", movechance="camp", capacity=49451, foreign=True))
  locations.append(e.addLocation("Nduta", movechance="default", capacity=55320, foreign=True)) # Nduta open on 2015-08-10
  locations.append(e.addLocation("Kagunga", movechance=1/21.0, foreign=True))
  locations.append(e.addLocation("Nyarugusu", movechance="camp", capacity=100925, foreign=True))
  locations.append(e.addLocation("Nakivale", movechance="camp", capacity=18734, foreign=True))
  locations.append(e.addLocation("Lusenda", movechance="default", capacity=17210, foreign=True))

  #Within Burundi
  e.linkUp("Bujumbura","Bubanza","48.0")
  e.linkUp("Bubanza","Bukinanyana","74.0")
  e.linkUp("Bujumbura","Cibitoke","63.0")
  e.linkUp("Cibitoke","Bukinanyana","49.0")
  e.linkUp("Bujumbura","Muramvya","58.0")
  e.linkUp("Muramvya","Gitega","44.0")
  e.linkUp("Gitega","Karuzi","54.0")
  e.linkUp("Gitega","Ruyigi","55.0")
  e.linkUp("Ruyigi","Karuzi","43.0")
  e.linkUp("Karuzi","Muyinga","42.0")
  e.linkUp("Bujumbura","Kayanza","95.0")
  e.linkUp("Kayanza","Ngozi","31.0") ##
  e.linkUp("Ngozi","Gashoho","41.0") ##
  e.linkUp("Kayanza","Kabarore","18.0")
  e.linkUp("Gashoho","Kirundo","42.0")
  e.linkUp("Gashoho","Muyinga","34.0")
  e.linkUp("Bujumbura","Mwaro","67.0")
  e.linkUp("Mwaro","Gitega","46.0")
  e.linkUp("Bujumbura","Rumonge","75.0")
  e.linkUp("Rumonge","Bururi","31.0")
  e.linkUp("Rumonge","Burambi","22.0")
  e.linkUp("Rumonge","Commune of Mabanda","73.0")
  e.linkUp("Commune of Mabanda","Makamba","18.0") # ??
  e.linkUp("Bururi","Rutana","65.0")
  e.linkUp("Makamba","Rutana","50.0") # ??
  e.linkUp("Rutana","Makebuko","46.0") # ??
  e.linkUp("Makebuko","Gitega","24.0") # ??
  e.linkUp("Makebuko","Ruyigi","40.0")
  e.linkUp("Ruyigi","Cankuzo","51.0")
  e.linkUp("Ruyigi","Gisuru","31.0")
  e.linkUp("Cankuzo","Muyinga","63.0")

  #Camps, starting at index locations[26] (at time of writing).
  e.linkUp("Muyinga","Mahama","135.0")
  e.linkUp("Kirundo","Mahama","183.0") #Shorter route than via Gashoho and Muyinga. Goes through Bugesera, where a transit centre is located according to UNHCR reports.
  e.linkUp("Gisuru","Nduta","60.0")
  e.linkUp("Commune of Mabanda","Kagunga","36.0")
  e.linkUp("Commune of Mabanda","Nyarugusu","71.0") #Estimated distance, as exact location of Nyarugusu is uncertain.

  e.linkUp("Kagunga","Nyarugusu","91.0", forced_redirection=True) #From Kagunga to Kigoma by ship (Kagunga=Kigoma)
  e.linkUp("Kirundo","Nakivale","318.0")
  e.linkUp("Kayanza","Nakivale","413.0")

  e.linkUp("Nduta","Nyarugusu","150.0", forced_redirection=True) #distance needs to be checked.

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="source_data/burundi2015", start_date="2015-05-01")

  # Correcting for overestimations due to inaccurate level 1 registrations in five of the camps.
  # These errors led to a perceived large drop in refugee population in all of these camps.
  # We correct by linearly scaling the values down to make the last level 1 registration match the first level 2 registration value.
  # To our knowledge, all level 2 registration procedures were put in place by the end of 2016.
  d.correctLevel1Registrations("Mahama","2015-10-04")
  d.correctLevel1Registrations("Nduta","2016-04-06")
  d.correctLevel1Registrations("Nyarugusu","2015-11-10")
  d.correctLevel1Registrations("Nakivale","2015-08-18")
  d.correctLevel1Registrations("Lusenda","2015-09-30")

  locations[26].capacity = d.getMaxFromData("Mahama", last_physical_day)
  locations[27].capacity = d.getMaxFromData("Nduta", last_physical_day)
  locations[29].capacity = d.getMaxFromData("Nyarugusu", last_physical_day)
  locations[30].capacity = d.getMaxFromData("Nakivale", last_physical_day)
  locations[31].capacity = d.getMaxFromData("Lusenda", last_physical_day)



  list_of_cities = "Time"

  for l in locations:
    list_of_cities = "%s,%s" % (list_of_cities, l.name)

  #print(list_of_cities)
  #print("Time, campname")
  print("Day,Mahama sim,Mahama data,Mahama error,Nduta sim,Nduta data,Nduta error,Nyarugusu sim,Nyarugusu data,Nyarugusu error,Nakivale sim,Nakivale data,Nakivale error,Lusenda sim,Lusenda data,Lusenda error,Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),refugee_debt,Total error (retrofitted)")


  #Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only


  e.add_conflict_zone("Bujumbura")


  t_retrofitted = 0

  for t in range(0,end_time):

    t_data = t

    #Lusenda camp open on the 30th of July 2015
    if t_data == date_to_sim_days("2015-07-30"): #Open Lusenda
      locations[31].SetCampMoveChance()
      locations[31].Camp=True
      e.linkUp("Bujumbura","Lusenda","53.0") #Only added when the refugee inflow starts at Lusenda, on 30-07-2015

    if t_data == date_to_sim_days("2015-08-10"):
      locations[27].SetCampMoveChance()
      locations[27].Camp=True
      e.remove_link("Nduta","Nyarugusu")
      e.linkUp("Nduta","Nyarugusu","150.0") #Re-add link, but without forced redirection


    #Append conflict_zone and weight to list.
    #Conflict zones after the start of simulation period
    if t_data == date_to_sim_days("2015-07-10"): #Intense fighting between military & multineer military forces
      e.add_conflict_zone("Kabarore")

    elif t_data == date_to_sim_days("2015-07-11"): #Intense fighting between military & mulineer military forces
      e.add_conflict_zone("Bukinanyana")

    elif t_data == date_to_sim_days("2015-07-15"): #Battles unidentified armed groups coordinately attacked military barracks
      e.add_conflict_zone("Cibitoke")

    elif t_data == date_to_sim_days("2015-10-26"): #Clashes and battles police forces
      e.add_conflict_zone("Mwaro")

    elif t_data == date_to_sim_days("2015-11-23"): #Battles unidentified armed groups coordinate attacks
      e.add_conflict_zone("Gisuru")

    elif t_data == date_to_sim_days("2015-12-08"): #Military forces
      e.add_conflict_zone("Burambi")

    #new_refs = d.get_new_refugees(t)
    new_refs = d.get_new_refugees(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_new_refugees(t, FullInterpolation=True)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    # Here we use the random choice to make a weighted choice between the source locations.
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

    #Propagate the model by one time step.
    e.evolve()

    #e.printInfo()

    #Validation/data comparison
    mahama_data = d.get_field("Mahama", t) #- d.get_field("Mahama", 0)
    nduta_data = d.get_field("Nduta", t) #-d.get_field("Nduta", 0)
    nyarugusu_data = d.get_field("Nyarugusu", t) #- d.get_field("Nyarugusu", 0)
    nakivale_data = d.get_field("Nakivale", t) #- d.get_field("Nakivale", 0)
    lusenda_data = d.get_field("Lusenda", t) #- d.get_field("Lusenda", 0)

    errors = []
    abs_errors = []
    loc_data = [mahama_data, nduta_data, nyarugusu_data, nakivale_data, lusenda_data]
    camp_locations = [26, 27, 29, 30, 31]

    camps = []
    for i in camp_locations:
      camps += [locations[i]]
    camp_names = ["Mahama", "Nduta", "Nyarugusu", "Nakivale", "Lusenda"]

    camp_pops_retrofitted = []
    errors_retrofitted = []
    abs_errors_retrofitted = []

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents
    t_retrofitted = d.retrofit_time_to_refugee_count(refugees_in_camps_sim, camp_names)

    # calculate errors
    for i in range(0,len(camp_locations)):
      camp_number = camp_locations[i]
      errors += [a.rel_error(locations[camp_number].numAgents, loc_data[i])]
      abs_errors += [a.abs_error(locations[camp_number].numAgents, loc_data[i])]

      # errors when using retrofitted time stepping.
      camp_pops_retrofitted += [d.get_field(camp_names[i], t_retrofitted, FullInterpolation=True)]
      errors_retrofitted += [a.rel_error(camps[i].numAgents, camp_pops_retrofitted[-1])]
      abs_errors_retrofitted += [a.abs_error(camps[i].numAgents, camp_pops_retrofitted[-1])]

    output = "%s" % t

    for i in range(0,len(errors)):
      camp_number = camp_locations[i]
      output += ",%s,%s,%s" % (locations[camp_number].numAgents, loc_data[i], errors[i])


    if refugees_raw>0:
      #output_string += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw)
      output += ",%s,%s,%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, t_retrofitted, refugees_in_camps_sim, refugee_debt, float(np.sum(abs_errors_retrofitted))/float(refugees_raw))
    else:
      output += ",0,0,0,0,0,0,0"
      #output_string += ",0"


    print(output)


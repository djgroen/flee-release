from flee import flee
from datamanager import handle_refugee_data
from datamanager import DataTable
import numpy as np
import outputanalysis.analysis as a
import analyze_graph
import sys

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

#Central African Republic (CAR) Simulation

def date_to_sim_days(date):
  return DataTable.subtract_dates(date,"2013-12-01")

def AddInitialRefugees(e, d, loc):
  """ Add the initial refugees to a location, using the location name"""
  num_refugees = int(d.get_field(loc.name, 0, FullInterpolation=True))
  for i in range(0, num_refugees):
    e.addAgent(location=loc)


if __name__ == "__main__":

  if len(sys.argv)>1:
    if (sys.argv[1]).isnumeric():
      end_time = int(sys.argv[1])
      last_physical_day = int(sys.argv[1])
    else:
      end_time = 820
      last_physical_day = 820
      duration = flee.SimulationSettings.SimulationSettings.ReadFromCSV(sys.argv[1])
      if duration>0:
        end_time = duration
        last_physical_day = end_time
  else:
    end_time = 820
    last_physical_day = 820

  RetroFitting = False
  if len(sys.argv)>2:
    if "-r" in sys.argv[2]:
      RetroFitting = True
      end_time *= 10

  e = flee.Ecosystem()

  #print("Conflict weight:",flee.SimulationSettings.SimulationSettings.ConflictWeight)

  #default movechance is 0.3

  lm = {}

  #CAR
  lm["Bangui"] = e.addLocation("Bangui", pop=734350-400000) #Subtracting the number of IDPs from the population to reflect local shelter.

  lm["Bimbo"] = e.addLocation("Bimbo", pop=267859)
  lm["Mbaiki"] = e.addLocation("Mbaiki")
  lm["Boda"] = e.addLocation("Boda", pop=11688)
  lm["Nola"] = e.addLocation("Nola", pop=41462)
  lm["Bossembele"] = e.addLocation("Bossembele", pop=37849)

  lm["Berberati"] = e.addLocation("Berberati", pop=105155)
  lm["Gamboula"] = e.addLocation("Gamboula")
  lm["Carnot"] = e.addLocation("Carnot", pop=54551)
  lm["Bouar"] = e.addLocation("Bouar", pop=39205)
  lm["Baboua"] = e.addLocation("Baboua")

  lm["Bozoum"] = e.addLocation("Bozoum", pop=22284)
  lm["Paoua"] = e.addLocation("Paoua", pop=17370)
  lm["Bossangoa"] = e.addLocation("Bossangoa", pop=38451)
  lm["RN1"] = e.addLocation("RN1", movechance=1.0) #non-city junction, Coordinates = 7.112110, 17.030220
  lm["Batangafo"] = e.addLocation("Batangafo", pop=16420)

  lm["Bouca"] = e.addLocation("Bouca", pop=12280)
  lm["Kabo"] = e.addLocation("Kabo")
  lm["Kaga Bandoro"] = e.addLocation("Kaga Bandoro", pop=27797)
  lm["Sibut"] = e.addLocation("Sibut", pop=24527)
  lm["Bamingui"] = e.addLocation("Bamingui", pop=6230)

  lm["Dekoa"] = e.addLocation("Dekoa", pop=12447)
  lm["Ndele"] = e.addLocation("Ndele", pop=13704)
  lm["Birao"] = e.addLocation("Birao")
  lm["Bria"] = e.addLocation("Bria", pop=43322)
  lm["Bambari"] = e.addLocation("Bambari", pop=41486)

  lm["Grimari"] = e.addLocation("Grimari", pop=10822)
  lm["Bangassou"] = e.addLocation("Bangassou", pop=35305)
  lm["Rafai"] = e.addLocation("Rafai", pop=13962)
  lm["Obo"] = e.addLocation("Obo", pop=36029)
  lm["Mobaye"] = e.addLocation("Mobaye")

  lm["Bohong"] = e.addLocation("Bohong", pop=19700)
  lm["Mbres"] = e.addLocation("Mbres", pop=20709)
  lm["Damara"] = e.addLocation("Damara", pop=32321)
  lm["Bogangolo"] = e.addLocation("Bogangolo", pop=9966)
  lm["Marali"] = e.addLocation("Marali")

  lm["Beboura"] = e.addLocation("Beboura")
  lm["RN8"] = e.addLocation("RN8", movechance=1.0) #non-city junction, Coordinates = 9.560670, 22.140450
  lm["Zemio"] = e.addLocation("Zemio")

  camp_movechance = flee.SimulationSettings.SimulationSettings.CampMoveChance

  #Chad, Cameroon & Demotratic R.of Congo & R. of Congo camps starting at index locations[39] (at time of writing).
  lm["Amboko"] = e.addLocation("Amboko", movechance=camp_movechance, capacity=12405, foreign=True)
  lm["Belom"] = e.addLocation("Belom", movechance=camp_movechance, capacity=28483, foreign=True)

  lm["Dosseye"] = e.addLocation("Dosseye", movechance=camp_movechance, capacity=22925, foreign=True)
  lm["Gondje"] = e.addLocation("Gondje", movechance=camp_movechance, capacity=12171, foreign=True)
  lm["Moyo"] = e.addLocation("Moyo", movechance=camp_movechance, capacity=10903, foreign=True) #strange blip in the data at 14969.
  lm["Lolo"] = e.addLocation("Lolo", movechance=1.0, foreign=True) #forwarding location (to aggreg. camp)
  lm["Mbile"] = e.addLocation("Mbile", movechance=1.0, foreign=True) #forwarding location (to aggreg. camp)

  lm["Batouri"] = e.addLocation("Batouri") #city on junction point
  lm["Timangolo"] = e.addLocation("Timangolo", movechance=1.0, foreign=True, x=4.628170000, y=14.544500000) #forwarding location (to aggreg. camp)
  lm["Gado-Badzere"] = e.addLocation("Gado-Badzere", movechance=1.0, foreign=True) #forwarding location (to aggreg. camp)
  lm["East"] = e.addLocation("East", movechance=camp_movechance, capacity=180485, foreign=True) #regional camp.
  lm["Borgop"] = e.addLocation("Borgop", movechance=1.0, foreign=True) #forwarding location (to aggreg. camp)

  lm["Ngam"] = e.addLocation("Ngam", movechance=1.0, foreign=True) #forwarding location (to aggreg. camp)
  lm["Adamaoua"] = e.addLocation("Adamaoua", movechance=camp_movechance, capacity=71506, foreign=True)
  lm["Mole"] = e.addLocation("Mole", movechance=camp_movechance, capacity=20454, foreign=True)
  lm["Gbadolite"] = e.addLocation("Gbadolite") #city on junction point
  lm["N24"] = e.addLocation("N24", movechance=1.0) #non-city junction, Coordinates = 3.610560, 20.762290

  lm["Bili"] = e.addLocation("Bili", movechance=camp_movechance, capacity=10282, foreign=True)
  #lm["Bossobolo"] = e.addLocation("Bossobolo", movechance=camp_movechance, capacity=18054, foreign=True) # excluded because Bossobolo has no measurable refugee influx.
  lm["Boyabu"] = e.addLocation("Boyabu", movechance=camp_movechance, capacity=20393, foreign=True)
  lm["Mboti"] = e.addLocation("Mboti", movechance=camp_movechance, capacity=704, foreign=True)
  lm["Inke"] = e.addLocation("Inke", movechance=camp_movechance, capacity=20365, foreign=True)

  lm["Betou"] = e.addLocation("Betou", movechance=camp_movechance, capacity=10232, foreign=True)
  lm["Brazaville"] = e.addLocation("Brazaville", movechance=camp_movechance, capacity=7221, foreign=True)
  lm["Gore"] = e.addLocation("Gore", movechance=1.0) #city on junction point, where refugees are actively encouraged to go to nearby camps.

  #Within CAR
  e.linkUp("Bangui","Bimbo","26.0")
  e.linkUp("Bimbo","Mbaiki","92.0")
  e.linkUp("Bangui","Boda","134.0")
  e.linkUp("Mbaiki","Boda","82.0")
  e.linkUp("Boda","Nola","221.0")
  e.linkUp("Boda","Bossembele","144.0")
  e.linkUp("Nola","Berberati","137.0")
  e.linkUp("Berberati","Gamboula","82.0")
  e.linkUp("Nola","Gamboula","148.0")
  e.linkUp("Berberati","Carnot","92.0")
  e.linkUp("Carnot","Bouar","140.0")
  e.linkUp("Bouar","Baboua","98.0")
  e.linkUp("Bouar","Bohong","72.0")
  e.linkUp("Bohong","Bozoum","101.0")
  e.linkUp("Bouar","Bozoum","109.0")
  e.linkUp("Bozoum","Carnot","186.0")
  e.linkUp("Bozoum","Paoua","116.0")
  e.linkUp("Paoua","Beboura","28.0")
  e.linkUp("Bozoum","Bossangoa","132.0")
  e.linkUp("Bossangoa","RN1","98.0")
  e.linkUp("Batangafo","RN1","154.0")
  e.linkUp("Beboura","RN1","54.0")
  e.linkUp("Bozoum","Bossembele","223.0")
  e.linkUp("Bossangoa","Bossembele","148.0")
  e.linkUp("Bossembele","Bogangolo","132.0")
  e.linkUp("Bossembele","Bangui","159.0")
  e.linkUp("Bossangoa","Bouca","98.0")
  e.linkUp("Bossangoa","Batangafo","147.0")
  e.linkUp("Bouca","Batangafo","84.0")
  e.linkUp("Batangafo","Kabo","60.0")
  e.linkUp("Kabo","Kaga Bandoro","107.0")
  e.linkUp("Batangafo","Kaga Bandoro","113.0")
  e.linkUp("Damara","Bogangolo","93.0")
  e.linkUp("Bangui","Damara","74.0")
  e.linkUp("Damara","Sibut","105.0")
  e.linkUp("Sibut","Bogangolo","127.0")
  e.linkUp("Bogangolo","Marali","55.0")
  e.linkUp("Marali","Bouca","58.0")
  e.linkUp("Marali","Sibut","89.0")
  e.linkUp("Sibut","Dekoa","69.0")
  e.linkUp("Dekoa","Kaga Bandoro","80.0")
  e.linkUp("Kaga Bandoro","Mbres","91.0")
  e.linkUp("Mbres","Bamingui","112.0")
  e.linkUp("Bamingui","Ndele","121.0")
  e.linkUp("Ndele","RN8","239.0")
  e.linkUp("RN8","Birao","114.0")
  e.linkUp("Birao","Bria","480.0")
  e.linkUp("Ndele","Bria","314.0")
  e.linkUp("Bria","Bambari","202.0")
  e.linkUp("Bambari","Grimari","77.0")
  e.linkUp("Grimari","Dekoa","136.0")
  e.linkUp("Grimari","Sibut","115.0")
  e.linkUp("Bria","Bangassou","282.0")
  e.linkUp("Bangassou","Rafai","132.0")
  e.linkUp("Bria","Rafai","333.0")
  e.linkUp("Rafai","Zemio","148.0")
  e.linkUp("Zemio","Obo","199.0")
  e.linkUp("Bangassou","Mobaye","224.0")
  e.linkUp("Mobaye","Bambari","213.0")
  e.linkUp("Mobaye","Gbadolite","146.0")
  e.linkUp("Gbadolite","Bangui","500.0")


  #CAR -> Chad
  e.linkUp("Kabo","Belom","89.0")
  e.linkUp("Beboura","Gore","87.0")
  e.linkUp("RN8","Moyo","186.0")

  # links within Chad
  e.linkUp("Gore","Amboko","6.0")
  #e.linkUp("Beboura","Amboko","93.0")
  e.linkUp("Gore","Gondje","15.0")
  #e.linkUp("Beboura","Gondje","102.0")
  #e.linkUp("Amboko","Gondje","7.0")
  #e.linkUp("Amboko","Dosseye","35.0")
  e.linkUp("Gore","Dosseye","34.0")
  #e.linkUp("Beboura","Dosseye","121.0")

  e.linkUp("Gamboula","Lolo","43.0")
  e.linkUp("Lolo","Mbile","11.0", forced_redirection=True)
  e.linkUp("Mbile","Batouri","56.0", forced_redirection=True)
  e.linkUp("Timangolo","Batouri","24.0", forced_redirection=True)
  e.linkUp("Batouri","East","27.0", forced_redirection=True)
  e.linkUp("Baboua","Gado-Badzere","81.0")
  e.linkUp("Gado-Badzere","Timangolo","211.0", forced_redirection=True)
  e.linkUp("Gado-Badzere","East","281.0", forced_redirection=True)
  e.linkUp("Paoua","Borgop","254.0")
  e.linkUp("Borgop","Ngam","44.0", forced_redirection=True)
  e.linkUp("Ngam","Adamaoua","272.0", forced_redirection=True)

  e.linkUp("Gbadolite","N24","93.0")
  #e.linkUp("N24","Bossobolo","23.0") #Bossobolo has been taken out (see above).
  e.linkUp("Bangui","Mole","42.0")
  e.linkUp("Mole","Boyabu","25.0")
  e.linkUp("Zemio","Mboti","174.0")
  e.linkUp("Mobaye","Mboti","662.0")
  e.linkUp("Gbadolite","Inke","42.0")
  e.linkUp("Mbaiki","Betou","148.0")
  e.linkUp("Nola","Brazaville","1300.0")

  #DEBUG: print graph and show it on an image.
  #vertices, edges = e.export_graph()
  #analyze_graph.print_graph_nx(vertices, edges, print_dist=True)
  #sys.exit()

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="source_data/car2014/", start_date="2013-12-01", data_layout="data_layout.csv")

  #Correcting for overestimations due to inaccurate level 1 registrations in five of the camps.
  #These errors led to a perceived large drop in refugee population in all of these camps.
  #We correct by linearly scaling the values down to make the last level 1 registration match the first level 2 registration value.
  #To our knowledge, all level 2 registration procedures were put in place by the end of 2016.
  d.correctLevel1Registrations("Amboko","2015-09-30")
  d.correctLevel1Registrations("Belom","2015-08-31")
  d.correctLevel1Registrations("Dosseye","2015-09-30")
  d.correctLevel1Registrations("Gondje","2015-09-30")
  lm["Moyo"].capacity *= d.correctLevel1Registrations("Moyo","2015-06-02") #also "2014-05-11" and "2015-06-02"
  d.correctLevel1Registrations("East","2014-09-28")
  d.correctLevel1Registrations("Adamaoua","2014-10-19")
  #d.correctLevel1Registrations("Mole","2016-02-29") # no clear decrease visible.
  d.correctLevel1Registrations("Bili","2016-06-30")
  #d.correctLevel1Registrations("Bossobolo","2016-05-20") #Data is only decreasing over time, so no grounds for a level1 corr.
  d.correctLevel1Registrations("Boyabu","2016-06-30")
  d.correctLevel1Registrations("Inke","2014-06-30")
  d.correctLevel1Registrations("Betou","2014-03-22")
  #d.correctLevel1Registrations("Brazaville","2016-04-30")

  lm["Amboko"].capacity = d.getMaxFromData("Amboko", last_physical_day)
  lm["Belom"].capacity = d.getMaxFromData("Belom", last_physical_day) # set manually.
  lm["Dosseye"].capacity = d.getMaxFromData("Dosseye", last_physical_day)
  lm["Gondje"].capacity = d.getMaxFromData("Gondje", last_physical_day)
  #lm["Moyo"].capacity = d.getMaxFromData("Moyo", last_physical_day ) # blip in the data set, set capacity manually.
  lm["East"].capacity = d.getMaxFromData("East", last_physical_day)
  lm["Adamaoua"].capacity = d.getMaxFromData("Adamaoua", last_physical_day)
  lm["Mole"].capacity = d.getMaxFromData("Mole", last_physical_day)
  lm["Bili"].capacity = d.getMaxFromData("Bili", last_physical_day)
  #lm["Bossobolo"].capacity = d.getMaxFromData("Bossobolo", last_physical_day) #camp excluded
  lm["Boyabu"].capacity = d.getMaxFromData("Boyabu", last_physical_day)
  lm["Mboti"].capacity = d.getMaxFromData("Mboti", last_physical_day)
  lm["Inke"].capacity = d.getMaxFromData("Inke", last_physical_day)
  lm["Betou"].capacity = d.getMaxFromData("Betou", last_physical_day)
  lm["Brazaville"].capacity = d.getMaxFromData("Brazaville", last_physical_day)


  camp_locations      = ["Amboko","Belom","Dosseye","Gondje","Moyo","East","Adamaoua","Mole","Bili","Boyabu","Mboti","Inke","Betou","Brazaville"]

  #for c in camp_locations:
  #  print(c, lm[c].capacity, d.getMaxFromData(c, last_physical_day))

  # Add initial refugees to the destinations.
  output_header_string = "Day,"

  for i in camp_locations:
    l = lm[i]
    AddInitialRefugees(e,d,l)
    output_header_string += "%s sim,%s data,%s error," % (l.name, l.name, l.name)

  output_header_string += "Total error,refugees in camps (UNHCR),total refugees (simulation),raw UNHCR refugee count,retrofitted time,refugees in camps (simulation),refugee_debt,Total error (retrofitted)"

  print(output_header_string)

  #Set up a mechanism to incorporate temporary decreases in refugees
  refugee_debt = 0
  refugees_raw = 0 #raw (interpolated) data from TOTAL UNHCR refugee count only

  #Append conflict_zones and weights to list from ACLED conflict database.
  #Conflict zones year before the start of simulation period
  #if t_data == date_to_sim_days("2012-12-10"):
  e.add_conflict_zone("Ndele")
  #if t_data == date_to_sim_days("2012-12-15"):
  e.add_conflict_zone("Bamingui")
  #if t_data == date_to_sim_days("2012-12-28"):
  e.add_conflict_zone("Bambari")
  #if t_data == date_to_sim_days("2013-01-18"):
  e.add_conflict_zone("Obo")
  #if t_data == date_to_sim_days("2013-03-11"):
  e.add_conflict_zone("Bangassou")
  #if t_data == date_to_sim_days("2013-03-24"):
  e.add_conflict_zone("Bangui") # Main capital entry. Bangui has 100,000s-500,000 IDPs though.
  #if t_data == date_to_sim_days("2013-04-17"):
  e.add_conflict_zone("Mbres")
  #if t_data == date_to_sim_days("2013-05-03"):
  e.add_conflict_zone("Bohong")
  #if t_data == date_to_sim_days("2013-05-17"):
  e.add_conflict_zone("Bouca")
  #if t_data == date_to_sim_days("2013-09-07"):
  e.add_conflict_zone("Bossangoa")
  #if t_data == date_to_sim_days("2013-09-14"):
  e.add_conflict_zone("Bossembele")
  #if t_data == date_to_sim_days("2013-10-10"):
  e.add_conflict_zone("Bogangolo")
  #if t_data == date_to_sim_days("2013-10-26"):
  e.add_conflict_zone("Bouar")
  #if t_data == date_to_sim_days("2013-11-10"):
  e.add_conflict_zone("Rafai")
  #if t_data == date_to_sim_days("2013-11-28"):
  e.add_conflict_zone("Damara")


  # Start with a refugee debt to account for the mismatch between camp aggregates and total UNHCR data.
  refugee_debt = e.numAgents()


  t_retrofitted = 0

  for t in range(0,end_time):

    e.refresh_conflict_weights()

    if RetroFitting==False:
      t_data = t
    else:
      t_data = int(t_retrofitted)
      if t_data > end_time / 10:
        break


    # Determine number of new refugees to insert into the system.
    new_refs = d.get_daily_difference(t, FullInterpolation=True) - refugee_debt
    refugees_raw += d.get_daily_difference(t, FullInterpolation=True)
    if new_refs < 0:
      refugee_debt = -new_refs
      new_refs = 0
    elif refugee_debt > 0:
      refugee_debt = 0

    new_links = []

    #CAR/DRC border is closed on the 5th of December 2013. Appears to remain closed until the 30th of June
    #Source: http://data.unhcr.org/car/download.php
    if t_data == date_to_sim_days("2013-12-05"):
      e.remove_link("Bangui","Mole")
      e.remove_link("Gbadolite","Inke")
      e.remove_link("Gbadolite","N24")
      e.remove_link("Zemio","Mboti")
      e.remove_link("Mobaye","Mboti")


    if t_data == date_to_sim_days("2014-06-30"):
      e.linkUp("Bangui","Mole","42.0")
      e.linkUp("Gbadolite","Inke","42.0")
      e.linkUp("Gbadolite","N24","93.0")
      e.linkUp("Zemio","Mboti","174.0")
      e.linkUp("Mobaye","Mboti","662.0")

    # 12 Feb. In Mole, refugees who were waiting to be registered and relocated received their food rations from the WFP.  
    # Source: http://data.unhcr.org/car/download.php?id=22

    # 19 Feb: drop of IDPs in Bangui from 400k to 273k.

    # Close borders here: On the 12th of May 2014, Chad closes border altogether.
    if t_data == date_to_sim_days("2014-05-12"):
      e.remove_link("Kabo","Belom")
      e.remove_link("Beboura","Gore")
      e.remove_link("RN8","Moyo")
      #Optional: write graph image for debugging purposes.
      #vertices, edges = e.export_graph()
      #analyze_graph.print_graph_nx(vertices, edges, print_dist=True)
      #sys.exit()

    # Bili camp opens on April 1st, 2015.
    if t_data == date_to_sim_days("2015-04-01"):
      e.linkUp("N24","Bili","20.0") #There is no road after 93km to the camp & the remaining 20km was found by distance calculator (www.movable-type.co.uk/scripts/latlong.html)
      #Optional: write graph image for debugging purposes.
      #vertices, edges = e.export_graph()
      #analyze_graph.print_graph_nx(vertices, edges, print_dist=True)


    #Conflict zones after the start of simulation period
    if t_data == date_to_sim_days("2013-12-06"): #A wave of reprisal attacks & escalating cycle of violence between Seleka militia and Anti-Balaka
      e.add_conflict_zone("Bozoum")

    #if t_data == date_to_sim_days("2013-12-21"): #MISCA: African-led International Support Mission against Anti-balaka (deaths & thousnads displaced)
    #  e.add_conflict_zone("Bossangoa")

    if t_data == date_to_sim_days("2014-01-01"): #Violence & death in battles between Seleka militia and Anti-Balaka
      e.add_conflict_zone("Bimbo")

    #if t_data == date_to_sim_days("2014-01-19"): #Violence & battles of Seleka militia with Anti-Balaka
    #  e.add_conflict_zone("Bambari")
    #if t_data == date_to_sim_days("2014-01-20"):
    #  e.add_conflict_zone("Bouar")

    if t_data == date_to_sim_days("2014-01-28"): #Battles between Seleka militia and Anti-Balaka
      e.add_conflict_zone("Boda")

    if t_data == date_to_sim_days("2014-02-06"): #Battles between Seleka militia and Anti-Balaka
      e.add_conflict_zone("Kaga Bandoro")

    if t_data == date_to_sim_days("2014-02-11"): ##Battles between Military forces and Anti-Balaka
      e.add_conflict_zone("Berberati")

    #if t_data == date_to_sim_days("2014-02-16"): #Battles between Seleka militia and Salanze Communal Militia
    #  e.add_conflict_zone("Bangassou")

    #if t_data == date_to_sim_days("2014-03-08"): #Battles between Seleka militia and Sangaris (French Mission)
    #  e.add_conflict_zone("Ndele")

    if t_data == date_to_sim_days("2014-03-11"): #MISCA: African-led International Support Mission against Anti-balaka
      e.add_conflict_zone("Nola")

    if t_data == date_to_sim_days("2014-04-08"): #Battles between Seleka militia and Anti-Balaka
      e.add_conflict_zone("Dekoa")

    if t_data == date_to_sim_days("2014-04-10"): #Battles of Bria Communal Militia (Seleka Militia) and MISCA (African-led International Support Mission)
      e.add_conflict_zone("Bria")

    if t_data == date_to_sim_days("2014-04-14"): #Battles between Anti-Balaka and Seleka militia
      e.add_conflict_zone("Grimari")

    #if t_data == date_to_sim_days("2014-04-23"): #Battles between Seleka militia and Anti-Balaka
    #  e.add_conflict_zone("Bouca")

    if t_data == date_to_sim_days("2014-04-26"): #Battles by unidentified Armed groups
      e.add_conflict_zone("Paoua")

    if t_data == date_to_sim_days("2014-05-23"): #MISCA: African-led International Support Mission against Anti-balaka
      e.add_conflict_zone("Carnot")

    if t_data == date_to_sim_days("2014-07-30"): #Battles between Anti-Balaka and Seleka militia
      e.add_conflict_zone("Batangafo")

    if t_data == date_to_sim_days("2014-10-10"): #MINUSCA: United Nations Multidimensional Integrated Stabilization Mission against Seleka militia (PRGF Faction)
      e.add_conflict_zone("Sibut")

    #Insert refugee agents
    for i in range(0, new_refs):
      e.addAgent(e.pick_conflict_location())

    #Propagate the model by one time step.
    e.evolve()

    #e.printInfo()

    #Calculation of error terms
    errors = []
    abs_errors = []
    loc_data = []

    camps = []
    for i in camp_locations:
      camps += [lm[i]]
      loc_data += [d.get_field(i, t)]

    camp_pops_retrofitted = []
    errors_retrofitted = []
    abs_errors_retrofitted = []

    # calculate retrofitted time.
    refugees_in_camps_sim = 0
    for c in camps:
      refugees_in_camps_sim += c.numAgents

    t_retrofitted = d.retrofit_time_to_refugee_count(refugees_in_camps_sim, camp_locations)

    # calculate errors
    j=0
    for i in camp_locations:
      errors += [a.rel_error(lm[i].numAgents, loc_data[j])]
      abs_errors += [a.abs_error(lm[i].numAgents, loc_data[j])]

      # errors when using retrofitted time stepping.
      camp_pops_retrofitted += [d.get_field(i, t_retrofitted, FullInterpolation=True)]
      errors_retrofitted += [a.rel_error(lm[i].numAgents, camp_pops_retrofitted[-1])]
      abs_errors_retrofitted += [a.abs_error(lm[i].numAgents, camp_pops_retrofitted[-1])]

      j += 1

    output = "%s" % t

    for i in range(0,len(errors)):
      output += ",%s,%s,%s" % (lm[camp_locations[i]].numAgents, loc_data[i], errors[i])


    if refugees_raw>0:
      #output_string += ",%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw)
      output += ",%s,%s,%s,%s,%s,%s,%s,%s" % (float(np.sum(abs_errors))/float(refugees_raw), int(sum(loc_data)), e.numAgents(), refugees_raw, t_retrofitted, refugees_in_camps_sim, refugee_debt, float(np.sum(abs_errors_retrofitted))/float(refugees_raw))
    else:
      output += ",0,0,0,0,0,0,0"
      #output_string += ",0"


    print(output)





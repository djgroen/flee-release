import csv
import sys
from flee import flee
from flee import SimulationSettings

class InputGeography:
  """
  Class which reads in Geographic information.
  """
  def __init__(self):
    self.locations = []
    self.links = []


  def ReadFlareConflictInputCSV(self,csv_name):
    """
    Reads a Flare input file, to set conflict information.
    """
    self.conflicts = {}

    row_count = 0
    headers = []

    with open(csv_name, newline='') as csvfile:
      values = csv.reader(csvfile)

      for row in values:
        #print(row)
        if row_count == 0:
          headers = row
          for i in range(1,len(headers)): # field 0 is day.
            headers[i] = headers[i].strip()
            if len(headers[i])>0:
              self.conflicts[headers[i]] = []
        else:
          for i in range(1,len(row)): # field 0 is day.
            #print(row[0])
            self.conflicts[headers[i]].append(int(row[i].strip()))
        row_count += 1

    #print(self.conflicts)
    ### TODO: make test verifying this in test_csv.py

  def getConflictLocationNames(self):
    return list(self.conflicts.keys())


  def ReadLocationsFromCSV(self,csv_name, columns=["name","region","country","gps_x","gps_y","location_type","conflict_date","pop/cap"]):
    """
    Converts a CSV file to a locations information table
    """
    self.locations = []

    c = {} #column map

    c["location_type"] = 0
    c["conflict_date"] = 0
    c["country"] = 0
    c["region"] = 0

    for i in range(0, len(columns)):
      c[columns[i]] = i

    with open(csv_name, newline='') as csvfile:
      values = csv.reader(csvfile)

      for row in values:
        if row[0][0] == "#":
          pass
        else:
          #print(row)
          self.locations.append([row[c["name"]], row[c["pop/cap"]], row[c["gps_x"]], row[c["gps_y"]], row[c["location_type"]], row[c["conflict_date"]], row[c["region"]], row[c["country"]]])


  def ReadLinksFromCSV(self,csv_name, name1_col=0, name2_col=1, dist_col=2):
    """
    Converts a CSV file to a locations information table
    """
    self.links = []

    with open(csv_name, newline='') as csvfile:
      values = csv.reader(csvfile)

      for row in values:
        if row[0][0] == "#":
          pass
        else:
          #print(row)
          self.links.append([row[name1_col], row[name2_col], row[dist_col]])

  def ReadClosuresFromCSV(self, csv_name):
    """
    Read the closures.csv file. Format is:
    closure_type,name1,name2,closure_start,closure_end
    """
    self.closures = []

    with open(csv_name, newline='') as csvfile:
      values = csv.reader(csvfile)

      for row in values:
        if row[0][0] == "#":
          pass
        else:
          #print(row)
          self.closures.append(row)

  def StoreInputGeographyInEcosystem(self, e):
    """
    Store the geographic information in this class in a FLEE simulation,
    overwriting existing entries.
    """
    lm = {}
    num_conflict_zones = 0

    for l in self.locations:
      if len(l[1]) < 1: #if population field is empty, just set it to 0.
        l[1] = "0"
      if len(l[7]) < 1: #if population field is empty, just set it to 0.
        l[7] = "unknown"

      #print(l, file=sys.stderr)
      movechance = l[4]
      if "conflict" in l[4].lower(): 
        num_conflict_zones += 1
        if int(l[5])>0:
          movechance = "town"

      if "camp" in l[4].lower():
        lm[l[0]] = e.addLocation(l[0], movechance=movechance, capacity=int(l[1]), x=l[2], y=l[3], country=l[7])
      else:
        lm[l[0]] = e.addLocation(l[0], movechance=movechance, pop=int(l[1]), x=l[2], y=l[3], country=l[7])

    for l in self.links:
        if (len(l)>3):
            if int(l[3]) == 1:
                e.linkUp(l[0], l[1], int(l[2]), True)
            if int(l[3]) == 2:
                e.linkUp(l[1], l[0], int(l[2]), True)
            else:
                e.linkUp(l[0], l[1], int(l[2]), False)
        else:
            e.linkUp(l[0], l[1], int(l[2]), False)

    e.closures = []
    for l in self.closures:
      e.closures.append([l[0], l[1], l[2], int(l[3]), int(l[4])])

    if num_conflict_zones < 1:
      print("Warning: location graph has 0 conflict zones (ignore if conflicts.csv is used).", file=sys.stderr)

    return e, lm

  def AddNewConflictZones(self, e, time, Debug=False):
    """
    Adds new conflict zones according to information about the current time step.
    If there is no Flare input file, then the values from locations.csv are used.
    If there is one, then the data from Flare is used instead.
    Note: there is no support for *removing* conflict zones at this stage.
    """
    if len(SimulationSettings.SimulationSettings.FlareConflictInputFile) == 0:
      for l in self.locations:
        if "conflict" in l[4].lower() and int(l[5]) == time:
          if e.print_location_output:
            print("Time = %s. Adding a new conflict zone [%s] with pop. %s" % (time, l[0], int(l[1])), file=sys.stderr)
          e.add_conflict_zone(l[0])
    else:
      confl_names = self.getConflictLocationNames()
      #print(confl_names)
      for l in confl_names:
        if Debug:
          print("L:", l, self.conflicts[l], time, file=sys.stderr)
        if self.conflicts[l][time] == 1:
          if time > 0:
            if self.conflicts[l][time-1] == 0:
              print("Time = %s. Adding a new conflict zone [%s]" % (time, l), file=sys.stderr)
              e.add_conflict_zone(l)
          else:
            print("Time = %s. Adding a new conflict zone [%s]" % (time, l), file=sys.stderr)
            e.add_conflict_zone(l)

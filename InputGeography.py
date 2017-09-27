import csv
import flee

class InputGeography:
  """
  Class which reads in Geographic information.
  """
  def __init__(self):
    self.locations = []
    self.links = []


  def ReadLocationsFromCSV(self,csv_name, name_col=0, population_col=2, gps_x_col=5, gps_y_col=6):
    """
    Converts a CSV file to a locations information table 
    """
    self.locations = []

    with open(csv_name, newline='') as csvfile:
      values = csv.reader(csvfile)

      for row in values:
        if row[0][0] == "#":
          pass
        else:
          #print(row)
          self.locations.append([row[name_col], row[population_col], row[gps_x_col], row[gps_y_col]])


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

  def StoreInputGeographyInEcosystem(self, e):
    """
    Store the geographic information in this class in a FLEE simulation, 
    overwriting existing entries.
    """
    lm = {}

    for l in self.locations:
      lm[l[0]] = e.addLocation(l[0], movechance=0.3, pop=int(l[1]), x=l[2], y=l[3])

    for l in self.links:
      e.linkUp(l[0], l[1], int(l[2]))

    return e, lm


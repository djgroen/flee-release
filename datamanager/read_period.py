import csv

def read_conflict_period(fname):
  """
  Reads in a conflict_period.csv file.
  """
  startdate = ""
  length = 0
  with open(fname) as csvfile:
    confl_reader = csv.reader(csvfile, delimiter=",")
    for row in confl_reader:
      if row[0].lower() == "startdate":
        startdate = row[1]
      if row[0].lower() == "length":
        length = int(row[1])
  return startdate, length

import csv

with open("refugees.csv", newline='') as csvfile:
    values = csv.reader(csvfile)
    first_line = True
    print(",")
    for row in values:

      if(first_line):
        first_line = False
        continue

      new_date = "%s-%s-%s,%s" % (row[0][6:10], row[0][3:5], row[0][0:2], row[1])

      print(new_date)



import numpy as np
import csv
from datamanager import DataTable
from datetime import datetime
import os.path

class RefugeeTable(DataTable.DataTable):

  def get_new_refugees(self, day, Debug=False, FullInterpolation=True):
    """
    This function is in place to provide an intuitive naming convention, and to retain backwards compatibility.
    See the corresponding function in DataTable.py for exact details on how to use it.
    """
    return self.get_daily_difference(day, day_column=0, count_column=1, Debug=Debug, FullInterpolation=FullInterpolation)

  def ReadL1Corrections(self, csvname):
    if os.path.isfile(csvname):  
      with open(csvname) as csvfile:
        l1reader = csv.reader(csvfile, delimiter=',')
        for row in l1reader:
          if len(row)>1:
            self.correctLevel1Registrations(row[0],row[1])

  def correctLevel1Registrations(self, name, date):
    """
    Corrects for level 1 registration overestimations. Returns the scaling factor
    """

    hindex = self._find_headerindex(name)
    days = DataTable.subtract_dates(date, self.start_date)
    ref_table = self.data_table[hindex]

    for i in range(0, len(ref_table)):
      if(int(ref_table[i][0]) == int(days)):
        # then scale all previous entries by ref_table[i][1]/ref_table[i-1][1]
        if i>0:
          first_level_2_value = ref_table[i,1]
          last_level_1_value  = ref_table[i-1,1]
          #print(days, i, ref_table[0:i,1])
          ref_table[0:i,1] *= first_level_2_value / last_level_1_value
          #print(first_level_2_value, last_level_1_value, ref_table[0:i,1])

    return first_level_2_value / last_level_1_value


  def getMaxFromData(self, name, days):
    """
    Gets the maximum refugee count in a certain place within the timespan of "days" days since the start date.
    """
    hindex = self._find_headerindex(name)
    ref_table = self.data_table[hindex]
    max_val = 0

    for i in range(0, len(ref_table)):

      if int(ref_table[i][0]) >= int(days):
        if int(ref_table[i,1]) > max_val:
          max_val = int(ref_table[i][1])
        break

      if int(ref_table[i,1]) > max_val:
        max_val = int(ref_table[i][1])

    return max_val


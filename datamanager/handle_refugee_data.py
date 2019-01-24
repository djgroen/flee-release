import numpy as np
import csv
from datamanager import DataTable
from datetime import datetime

class RefugeeTable(DataTable.DataTable):

  def retrofit_time_to_refugee_count(self, refugee_count, camp_names):
    """
    Takes the total refugee count in camps (from simulation), and determines at which time this number of refugees
    are found in the data. It then returns this time, which can be fractional.
    refugee_count: number of refugees in camps in the simulation, and the value we seek to match time against.
    camp_names: list of names (strings) of the refugee camp locations.
    TODO: make camp_names list auto-detectable in the simulation.

    LIMITATION: This approach assumes a continual increase in refugee populations. Long-term decreasing trends
    in the data will cause the function to return garbage.
    """

    last_data_count = 0
    initial_data_count = 0
    last_t = 0
    last_time_in_data = int(self.data_table[0][-1][self.days_column])
    #print("LAST TIME IN DATA = ", int(self.data_table[0][-1][self.days_column]))

    for name in camp_names:
      # aggregate refugee counts from all camps in the simulation
      initial_data_count += self.get_field(name , 0)
    last_data_count = initial_data_count

    if refugee_count <= initial_data_count:
      return 0

    for t in range(1, last_time_in_data-1):
      data_count = 0
      for name in camp_names:
        # aggregate refugee counts from all camps in the simulation
        data_count += self.get_field(name , t)
        #print("Name: ", name, "Camp pop. ", self.get_field(name , t))

      #print(last_data_count, refugee_count, data_count)

      if int(refugee_count) >= int(last_data_count):
        if int(data_count) >= int(refugee_count):
          # the current entry in the table has a number that exceeds the refugee count we're looking for.
          # action: interpolate between current and last entry to get the accurate fractional time.
          t_frac = float(refugee_count - last_data_count) / float(data_count - last_data_count)
          #print("RETURN t_corr = ", last_t + t_frac * (t - last_t), ", t = ", t, ", last_t = ", last_t, ", refugees in data = ", data_count, "refugees in sim = ", refugee_count)
          return last_t + t_frac * (t - last_t)

      if int(data_count) >= int(last_data_count):
        # Only when the current refugee count in the data exceeds the highest one found previously,
        # will we make a new interpolation checkpoint.
        last_data_count = data_count
        last_t = t


    print("Retrofit output:", refugee_count, last_time_in_data, last_data_count, initial_data_count, data_count)
    sys.exit()
    return last_time_in_data


  def get_new_refugees(self, day, Debug=False, FullInterpolation=True):
    """
    This function is in place to provide an intuitive naming convention, and to retain backwards compatibility.
    See the corresponding function in DataTable.py for exact details on how to use it.
    """
    return self.get_daily_difference(day, day_column=0, count_column=1, Debug=Debug, FullInterpolation=FullInterpolation)

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


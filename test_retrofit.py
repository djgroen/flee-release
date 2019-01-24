import flee.flee as flee
import datamanager.handle_refugee_data as handle_refugee_data
import numpy as np
import outputanalysis.analysis as a

"""
Generation 1 code. Incorporates only distance, travel always takes one day.
"""

if __name__ == "__main__":
  print("Testing basic data handling and simulation kernel.")

  d = handle_refugee_data.RefugeeTable(csvformat="generic", data_directory="mali2012/")

  camp_names = ["Mbera", "Fassala", "Mentao", "Bobo-Dioulasso", "Abala", "Mangaize", "Niamey", "Tabareybarey"]
  # TODO: refactor camp_names using list comprehension.

  for refugees_in_camps_sim in [50000,100000,130000]: 
    t_retrofitted = d.retrofit_time_to_refugee_count(refugees_in_camps_sim, camp_names)
    print(refugees_in_camps_sim, t_retrofitted)


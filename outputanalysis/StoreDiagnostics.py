import numpy as np

class LocationErrors:
  """
  Class containing a dictionary of errors and diagnostics pertaining a single location.
  """
  def __init__(self):
    self.errors = {}


class SimulationErrors:
  """
  Class containing all error measures within a single simulation.
  It should be initialized with a Python list of the LocationErrors structure
  for all of the relevant locations.
  """
  def __init__(self, location_errors):
    self.location_errors = location_errors


  def abs_diff(self, rescaled=True):
    #true_total_refs is the number of total refugees according to the data.

    errtype = "absolute difference"
    if rescaled:
      errtype = "absolute difference rescaled"

    self.tmp = self.location_errors[0].errors[errtype]

    for lerr in self.location_errors[1:]:
      self.tmp = np.add(self.tmp, lerr.errors[errtype])

    return self.tmp

  def get_error(self, err_type):
    """
    Here err_type is the string name of the error that needs to be aggregated.
    """
    self.tmp = self.location_errors[0].errors[err_type] * self.location_errors[0].errors["N"]
    N = self.location_errors[0].errors["N"]

    for lerr in self.location_errors[1:]:
      self.tmp = np.add(self.tmp, lerr.errors[err_type] * lerr.errors["N"])
      N += lerr.errors["N"]

    #print(self.tmp, N, self.tmp/ N)
    return self.tmp / N

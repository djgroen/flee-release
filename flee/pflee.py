#pflee.py
# A parallelized implementation of FLEE (with original rules)
#example to run: mpiexec -n 4 python3 pflee.py 100
import numpy as np
import sys
import random
from flee.SimulationSettings import SimulationSettings
from flee import flee
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

class MPIManager:
  def __init__(self):
    if not MPI.Is_initialized():
      print("Manual MPI_Init performed.")
      MPI.Init()
    self.comm = MPI.COMM_WORLD
    self.rank = self.comm.Get_rank()
    self.size = self.comm.Get_size()

  def CalcCommWorldTotalSingle(self, i):

    total = np.array([-1])
    # If you want this number on rank 0, just use Reduce.
    self.comm.Allreduce(np.array([i]), total, op=MPI.SUM)
    return total[0]

  def CalcCommWorldTotal(self, np_array):
    assert np_array.size > 0

    total = np.zeros(np_array.size, dtype='i')

    #print(self.rank, type(total), type(np_array), total, np_array, np_array.size)
    # If you want this number on rank 0, just use Reduce.
    self.comm.Allreduce([np_array, MPI.INT], [total, MPI.INT], op=MPI.SUM)

    return total


class Person(flee.Person):

  __slots__ = ['location', 'home_location', 'timesteps_since_departure', 'places_travelled', 'recent_travel_distance', 'distance_moved_this_timestep', 'travelling', 'distance_travelled_on_link', 'e']

  def __init__(self, e, location):
    super().__init__(location)
    self.e = e

  def evolve(self, ForceTownMove=False):
    super().evolve(ForceTownMove)


  def finish_travel(self):
    super().finish_travel()


  def getLinkWeight(self, link, awareness_level):
    """
    Calculate the weight of an adjacent link. Weight = probability that it will be chosen.
    """

    # If turning back is NOT allowed, remove weight from the last location.
    if not SimulationSettings.TurnBackAllowed:
      if link.endpoint == self.last_location:
        return 0.0 #float(0.1 / float(SimulationSettings.Softening + link.distance))

    if awareness_level < 0:
      return 1.0


    return float(self.e.scores[(link.endpoint.id * 4) + awareness_level] / float(SimulationSettings.Softening + link.distance))


  def getEndPointScore(self, link):
    """
    Overwrite serial function because we have a different data structure for endpoint scores.
    """
    return float(self.e.scores[(link.endpoint.id * 4) + 1])



class Location(flee.Location):

  def __init__(self, e, cur_id, name, x=0.0, y=0.0, movechance=0.001, capacity=-1, pop=0, foreign=False, country="unknown"):
    self.e = e

    self.id = cur_id
    self.numAgentsSpawnedOnRank = 0

    # If it is referred to in Flee in any way, the code should crash.
    super().__init__(name, x, y, movechance, capacity, pop, foreign, country)

    self.scores = [] # Emptying this array, as it is not used in the parallel version.

  def DecrementNumAgents(self):
    self.numAgentsOnRank -= 1


  def IncrementNumAgents(self):
    self.numAgentsOnRank += 1


  def print(self):
    if self.e.mpi.rank == 0:
      super().print() 


  def getScore(self, index):
    return self.e.scores[self.id * self.e.scores_per_location + index]

  def setScore(self, index, value):
    self.e.scores[self.id * self.e.scores_per_location + index]= value


  def updateAllScores(self, time):
    """ Updates all scores of a particular location. Different to Serial Flee, due to the reversed order there. """
    self.time = time
    self.updateRegionScore()
    self.updateNeighbourhoodScore()
    self.updateLocationScore()


class Link(flee.Link):

  def __init__(self, endpoint, distance, forced_redirection=False):
    super().__init__(endpoint, distance, forced_redirection)

  def DecrementNumAgents():
    self.numAgentsOnRank -= 1

  def IncrementNumAgents():
    self.numAgentsOnRank += 1


class Ecosystem(flee.Ecosystem):
  def __init__(self):


    self.locations = []
    self.locationNames = []
    self.agents = []
    self.total_agents = 0
    self.closures = [] #format [type, source, dest, start, end]
    self.time = 0
    self.print_location_output = False
    self.mpi = MPIManager()

    if self.getRankN(0):
      print("Creating Flee Ecosystem.", file=sys.stderr)

    self.cur_loc_id = 0
    self.scores_per_location = 4
    self.scores = np.array([1.0,1.0,1.0,1.0]) # single array holding all the location-related scores.


    # Bring conflict zone management into FLEE.
    self.conflict_zones = []
    self.conflict_zone_names = []
    self.conflict_weights = np.array([])
    self.conflict_pop = 0

    self.parallel_mode = "loc-par" # classic for replicated locations or loc-par for distributed locations.
    self.latency_mode = "high_latency" # high_latency for fewer MPI calls with more prep, or low_latency for more MPI calls with less prep.

    if SimulationSettings.CampLogLevel > 0:
      self.num_arrivals = [] # one element per time step.
      self.travel_durations = [] # one element per time step.

  def getRankN(self, t):
    """
    Returns the <rank N> value, which is the rank meant to perform diagnostics at a given time step.
    Argument t contains the current number of time steps taken by the simulation.
    NOTE: This is overwritten to just give rank 0, to prevent garbage output ordering...
    """
    #N = t % self.mpi.size
    #if self.mpi.rank == N:
    if self.mpi.rank == 0:
      return True
    return False

  def updateNumAgents(self, CountClosed=False, mode="high_latency"):
    total = 0

    if mode=="low_latency":
      for loc in self.locations:
        loc.numAgents = self.mpi.CalcCommWorldTotalSingle(loc.numAgentsOnRank)
        total += loc.numAgents
        #print("location:", self.time, loc.name, loc.numAgents, file=sys.stderr)
        for link in loc.links:
          link.numAgents = self.mpi.CalcCommWorldTotalSingle(link.numAgentsOnRank)
          #print(self.time, "link:", loc.name, link.numAgents, file=sys.stderr)
          total += link.numAgents
        if CountClosed:
          for link in loc.closed_links:
            link.numAgents = self.mpi.CalcCommWorldTotalSingle(link.numAgentsOnRank)
            #print(self.time, "link [closed]:", loc.name, link.numAgents, file=sys.stderr)
            total += link.numAgents
      self.total_agents = total
    elif mode == "high_latency":
      buf_len = 0
        
      buf_len += len(self.locations)
      for loc in self.locations:
          buf_len += len(loc.links)
          if CountClosed:
            buf_len += len(loc.closed_links)
       
      numAgent_buffer = np.empty(buf_len, dtype='i')
      new_buffer = np.empty(buf_len, dtype='i')

      index = 0
      for loc in self.locations:
        numAgent_buffer[index] = loc.numAgentsOnRank
        index += 1
        for link in loc.links:
          numAgent_buffer[index] = link.numAgentsOnRank
          index += 1
        if CountClosed:
          for link in loc.closed_links:
            numAgent_buffer[index] = link.numAgentsOnRank
            index += 1
            
      new_buffer = self.mpi.CalcCommWorldTotal(numAgent_buffer)

      index = 0
      for loc in self.locations:
        loc.numAgents = new_buffer[index]
        index += 1
        for link in loc.links:
          link.numAgents = new_buffer[index]
          index += 1
        if CountClosed:
          for link in loc.closed_links:
            link.numAgents = new_buffer[index]
            index += 1
            
      self.total_agents = np.sum(new_buffer)

    if self.mpi.rank == 0:
      print("Total agents in simulation:", self.total_agents, file=sys.stderr)


  """
  Add & insert agent functions.
  TODO: make addAgent function smarter, to prevent large load imbalances over time
  due to removals by clearLocationFromAgents?
  """

  def addAgent(self, location):
    if SimulationSettings.TakeRefugeesFromPopulation:
      if location.conflict:  
        if location.pop > 1:
          location.pop -= 1
          location.numAgentsSpawnedOnRank += 1
          location.numAgentsSpawned += 1
        else:
          print("ERROR: Number of agents in the simulation is larger than the combined population of the conflict zones. Please amend locations.csv.")
          location.print()
          assert location.pop > 1
    self.total_agents += 1
    if self.total_agents % self.mpi.size == self.mpi.rank:
      self.agents.append(Person(self, location))

  def insertAgent(self, location):
    """
    Note: insert Agent does NOT take from Population.
    """
    self.total_agents += 1
    if self.total_agents % self.mpi.size == self.mpi.rank:
      self.agents.append(Person(self, location))

  def insertAgents(self, location, number):
    for i in range(0,number):
      self.insertAgent(location)


  def clearLocationsFromAgents(self, location_names): #TODO:REWRITE!!
    """
    Remove all agents from a list of locations by name.
    Useful for couplings to other simulation codes.
    """

    new_agents = []
    for i in range(0, len(self.agents)):
      if self.agents[i].location.name not in location_names:
        new_agents += [self.agents[i]]
      else:
        #print("Agent removed: ", self.agents[i].location.name)
        self.agents[i].location.numAgentsOnRank -= 1 #agent is removed from ecosystem and number of agents in location drops by one.

    self.agents = new_agents
    print("clearLocationsFromAgents()", file=sys.stderr)
    self.updateNumAgents() # when numAgentsOnRank has changed, we need to updateNumAgents (1x MPI_Allreduce)


  def numAgents(self):
    return self.total_agents

  def numAgentsOnRank(self):
    return len(self.agents)

  def synchronize_locations(self, start_loc_local, end_loc_local, Debug=False):
      """
      Gathers the scores from all the updated locations, and propagates them across the processes.
      """

      base = int((len(self.scores)/self.scores_per_location) / self.mpi.size)
      leftover = int((len(self.scores)/self.scores_per_location) % self.mpi.size)

      if Debug:
        print("Sync Locs:", self.mpi.rank, base, leftover, len(self.scores), file=sys.stderr)

      sizes = np.ones(self.mpi.size, dtype='i')*base
      sizes[:leftover] += 1
      sizes *= self.scores_per_location
      offsets = np.zeros(self.mpi.size, dtype='i')
      offsets[1:] = np.cumsum(sizes)[:-1]

      assert np.sum(sizes) == len(self.scores)
      assert offsets[-1] + sizes[-1] == len(self.scores)

      # Populate scores array
      scores_start = int(offsets[self.mpi.rank])
      local_scores_size = int(sizes[self.mpi.rank])
      local_scores = self.scores[scores_start:scores_start+local_scores_size].copy()

      if Debug and self.mpi.rank == 0:
        print("start of synchronize_locations MPI call.", file=sys.stderr)
        #print(self.mpi.rank, local_scores, self.scores, sizes, offsets)
      self.mpi.comm.Allgatherv(local_scores, [self.scores, sizes, offsets, MPI.DOUBLE])

      if Debug and self.mpi.rank == 0:
        print("end of synchronize_locations", file=sys.stderr)

  def evolve(self):
    if self.time == 0:
        #print("rank, num_agents:", self.mpi.rank, len(self.agents))

        # Update all scores three times to ensure code starts with updated scores.
        for times in range(0, 3):
          for i in range(0, len(self.locations)):
            if i % self.mpi.size == self.mpi.rank:
              self.locations[i].updateAllScores(self.time)

    if self.parallel_mode == "classic":
      # update level 1, 2 and 3 location scores.
      # Scores remain perfectly updated in classic mode.
      for l in self.locations:
        l.time = self.time
        l.updateLocationScore()

      for l in self.locations:
        l.updateNeighbourhoodScore()

      for l in self.locations:
        l.updateRegionScore()

    elif self.parallel_mode == "loc-par":
      # update scores in reverse order for efficiency.
      # Neighbourhood and Region score will be outdated by 1 and 2 time steps resp.
      
      loc_per_rank = int(len(self.locations) / self.mpi.size)
      lpr_remainder = int(len(self.locations) % self.mpi.size)

      offset = int(self.mpi.rank) * int(loc_per_rank) + int(min(self.mpi.rank, lpr_remainder))
      num_locs_on_this_rank = int(loc_per_rank)
      if self.mpi.rank < lpr_remainder:
        num_locs_on_this_rank += 1

      for i in range(offset, offset + num_locs_on_this_rank):
        self.locations[i].updateAllScores(self.time)

      self.synchronize_locations(offset, offset + num_locs_on_this_rank)

    # SYNCHRONIZE SPAWN COUNTS IN LOCATIONS (needed for all versions).
    spawn_counts = np.zeros(len(self.locations), dtype='i')
    for i, le in enumerate(self.locations):
      #print(i, spawn_counts.size)
      spawn_counts[i] = le.numAgentsSpawnedOnRank

    #allreduce (sum up) spawn counts.
    spawn_totals = self.mpi.CalcCommWorldTotal(spawn_counts)
    
    #update location spawn total.
    for i, le in enumerate(self.locations):
      le.numAgentsSpawned = spawn_totals[i]

    #update agent locations
    for a in self.agents:
      a.evolve()

    #print("NumAgents after evolve:", file=sys.stderr)
    self.updateNumAgents(CountClosed = True)

    for a in self.agents:
      a.finish_travel()
      a.timesteps_since_departure += 1
      a.recent_travel_distance = (a.recent_travel_distance + ( a.distance_moved_this_timestep / SimulationSettings.MaxMoveSpeed )) / 2.0
      a.distance_moved_this_timestep = 0

    #print("NumAgents after finish_travel:", file=sys.stderr)
    self.updateNumAgents(mode=self.latency_mode)

    #update link properties
    if SimulationSettings.CampLogLevel > 0:
      self._aggregate_arrivals()

    self.time += 1

  def addLocation(self, name, x="0.0", y="0.0", movechance=SimulationSettings.DefaultMoveChance, capacity=-1, pop=0, foreign=False, country="unknown"):
    """ Add a location to the ABM network graph """

    # Enlarge the scores array in Ecosystem to reflect the new location. Pflee only.
    if self.cur_loc_id > 0:
      self.scores = np.append(self.scores, np.array([1.0,1.0,1.0,1.0]))
    #print(len(self.scores))

    l = Location(self, self.cur_loc_id, name, x, y, movechance, capacity, pop, foreign, country)

    self.cur_loc_id += 1

    if SimulationSettings.InitLogLevel > 0:
      print("Location:", name, x, y, l.movechance, capacity, ", pop. ", pop, foreign, file=sys.stderr)
    self.locations.append(l)
    self.locationNames.append(l.name)
    return l

  def printComplete(self):
    if self.mpi.rank == 0:
      super().printComplete() 

  def printInfo(self):
    if self.mpi.rank == 0:
      super().printInfo() 

if __name__ == "__main__":
  print("No testing functionality here yet.")

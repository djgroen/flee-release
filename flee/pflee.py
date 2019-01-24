#pflee.py
# A parallelized implementation of FLEE (with original rules)
#example to run: mpiexec -n 4 python3 pflee.py 100
import numpy as np
import sys
import random
from flee import SimulationSettings
from flee import flee
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE


class MPIManager:
  def __init__(self):
    self.comm = MPI.COMM_WORLD
    self.rank = self.comm.Get_rank()
    self.size = self.comm.Get_size()

  def CalcCommWorldTotal(self, i):
    total = np.array([-1])
    self.comm.Allreduce(np.array([i]), total, op=MPI.SUM)
    #total = self.CalcCommWorldTotalOnRank0(i)
    #total = self.comm.bcast(np.array([total]), root=0)
    #total = total[0]
    #print("Rank, Total: ", self.rank, total)
    return total[0]

  def CalcCommWorldTotalOnRank0(self, number):

    total = -1
    num_buf = np.array([number])
    # communication
    # Rank 0 receives results from all ranks and sums them
    if self.rank == 0:
      recv_buf = np.zeros(1)
      total = number
      for i in range(1, self.size):
        self.comm.Recv(recv_buf, ANY_SOURCE)
        total += recv_buf[0]
      return total
    else:
      self.comm.Send(num_buf,0)

class Person(flee.Person):
  def __init__(self, location):
    super().__init__(location)
    self.location.numAgentsOnRank += 1

  def evolve(self):

    if self.travelling == False:
      movechance = self.location.movechance

      outcome = random.random()
      if outcome < movechance:
        # determine here which route to take?
        chosenRoute = self.selectRoute()

        # if there is a viable route to a different location.
        if chosenRoute >= 0:
          # update location to link endpoint
          self.location.numAgentsOnRank -= 1
          self.location = self.location.links[chosenRoute]
          self.location.numAgentsOnRank += 1
          self.travelling = True
          self.distance_travelled_on_link = 0

    self.timesteps_since_departure += 1


  def finish_travel(self, distance_moved_this_timestep=0):
    if self.travelling:

      # update last location of agent.
      #if not SimulationSettings.SimulationSettings.TurnBackAllowed:
      #  self.last_location = self.location

      self.distance_travelled_on_link += SimulationSettings.SimulationSettings.MaxMoveSpeed

      # If destination has been reached.
      if self.distance_travelled_on_link - distance_moved_this_timestep > self.location.distance:

        # update agent logs
        if SimulationSettings.SimulationSettings.AgentLogLevel > 0:
          self.places_travelled += 1
          self.distance_travelled += self.location.distance

        # if the person has moved less than the minMoveSpeed, it should go through another evolve() step in the new location.
        evolveMore = False
        if self.location.distance + distance_moved_this_timestep < SimulationSettings.SimulationSettings.MinMoveSpeed:
          distance_moved_this_timestep += self.location.distance
          evolveMore = True

        # update location (which is on a link) to link endpoint
        self.location.numAgentsOnRank -= 1
        self.location = self.location.endpoint
        self.location.numAgentsOnRank += 1

        self.travelling = False
        self.distance_travelled_on_link = 0

        if SimulationSettings.SimulationSettings.CampLogLevel > 0:
          if self.location.Camp == True:
            self.location.incoming_journey_lengths += [self.timesteps_since_departure]

        # Perform another evolve step if needed. And if it results in travel, then the current
        # travelled distance needs to be taken into account.
        if evolveMore == True:
          self.evolve()
          self.finish_travel(distance_moved_this_timestep)



class Location(flee.Location):
  pass
  #code below is deprecated, as I added the variable to flee.py instead to retain easy compatibility with the CSV framework (same for Link).
  #I may wish to revise this design decision in the future.
  #def __init__(self, name, x=0.0, y=0.0, movechance=0.001, capacity=-1, pop=0, foreign=False, country="unknown"):
  #  self.numAgentsOnRank = 0
  #  super().__init__(name, x, y, movechance, capacity, pop, foreign, country)

class Link(flee.Link):
  pass
  #def __init__(self, endpoint, distance, forced_redirection=False):
  #  self.numAgentsOnRank = 0
  #  super().__init__(endpoint, distance, forced_redirection)

class Ecosystem(flee.Ecosystem):
  def __init__(self):
    self.locations = []
    self.locationNames = []
    self.agents = []
    self.total_agents = 0
    self.closures = [] #format [type, source, dest, start, end]
    self.time = 0
    self.mpi = MPIManager()

    # Bring conflict zone management into FLEE.
    self.conflict_zones = []
    self.conflict_zone_names = []
    self.conflict_weights = np.array([])
    self.conflict_pop = 0

    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      self.num_arrivals = [] # one element per time step.
      self.travel_durations = [] # one element per time step.

  def getRankN(self, t):
    """
    Returns the <rank N> value, which is the rank meant to perform diagnostics at a given time step.
    Argument t contains the current number of time steps taken by the simulation.
    """
    N = t % self.mpi.size
    if self.mpi.rank == N:
      return True
    return False

  def updateNumAgents(self):
    total = 0
    for loc in self.locations:
      loc.numAgents = self.mpi.CalcCommWorldTotal(loc.numAgentsOnRank)
      total += loc.numAgents
      #print("location:", loc.name, loc.numAgents)
      for link in loc.links:
        link.numAgents = self.mpi.CalcCommWorldTotal(link.numAgentsOnRank)
        #print("location link:", loc.name, link.numAgents)
        total += link.numAgents
    self.total_agents = total
    print("Total agents in simulation:", total, file=sys.stderr)


  """
  Add & insert agent functions.
  TODO: make addAgent function smarter, to prevent large load imbalances over time
  due to removals by clearLocationFromAgents?
  """

  def addAgent(self, location):
    if SimulationSettings.SimulationSettings.TakeRefugeesFromPopulation:
      if location.pop > 0:
        location.pop -= 1
    self.total_agents += 1
    if self.total_agents % self.mpi.size == self.mpi.rank:
      self.agents.append(Person(location))

  def insertAgent(self, location):
    """
    Note: insert Agent does NOT take from Population.
    """
    self.total_agents += 1
    if self.total_agents % self.mpi.size == self.mpi.rank:
      self.agents.append(Person(location))

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
    self.updateNumAgents() # when numAgentsOnRank has changed, we need to updateNumAgents (1x MPI_Allreduce)


  def numAgents(self):
    return self.total_agents

  def numAgentsOnRank(self):
    return len(self.agents)

  def evolve(self):
    if self.time == 0:
        print("rank, num_agents:", self.mpi.rank, len(self.agents))

    # update level 1, 2 and 3 location scores
    for l in self.locations:
      l.updateLocationScore(self.time)

    for l in self.locations:
      l.updateNeighbourhoodScore()

    for l in self.locations:
      l.updateRegionScore()

    #update agent locations
    for a in self.agents:
      a.evolve()

    self.updateNumAgents()

    for a in self.agents:
      a.finish_travel()

    self.updateNumAgents()

    #update link properties
    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      self._aggregate_arrivals()

    self.time += 1


if __name__ == "__main__":
  print("No testing functionality here yet.")

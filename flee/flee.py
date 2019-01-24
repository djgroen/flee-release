import random
import numpy as np
import csv
import sys
import copy
#from multiprocessing import Process,Pool
from flee import SimulationSettings

class Person:
  def __init__(self, location):
    self.health = 1

    self.injured = 0

    self.age = 35
    self.location = location
    self.home_location = location
    self.location.numAgents += 1
    self.timesteps_since_departure = 0

    # Set to true when an agent resides on a link.
    self.travelling = False

    # Tracks how much distance a Person has been able to travel on the current link.
    self.distance_travelled_on_link = 0

    #if not SimulationSettings.SimulationSettings.TurnBackAllowed:
    #  self.last_location = None

    if SimulationSettings.SimulationSettings.AgentLogLevel > 0:
      self.distance_travelled = 0
      self.places_travelled = 1

  def evolve(self):

    if self.travelling == False:
      movechance = self.location.movechance

      outcome = random.random()
      #print(movechance)

      if outcome < movechance:
        # determine here which route to take?
        chosenRoute = self.selectRoute()

        # if there is a viable route to a different location.
        if chosenRoute >= 0:
          # update location to link endpoint
          self.location.numAgents -= 1
          self.location = self.location.links[chosenRoute]
          self.location.numAgents += 1
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
        self.location.numAgents -= 1
        self.location = self.location.endpoint
        self.location.numAgents += 1

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

  def getLinkWeight(self, link, awareness_level):
    """
    Calculate the weight of an adjacent link. Weight = probability that it will be chosen.
    """

    # If turning back is NOT allowed, remove weight from the last location.
    #if not SimulationSettings.SimulationSettings.TurnBackAllowed:
    #  if link.endpoint == self.last_location:
    #    return 0.0 #float(0.1 / float(SimulationSettings.SimulationSettings.Softening + link.distance))

    if awareness_level < 0:
      return 1.0

    return float(link.endpoint.scores[awareness_level] / float(SimulationSettings.SimulationSettings.Softening + link.distance))

  def selectRoute(self):
    linklen = len(self.location.links)
    weights = np.zeros(linklen)

    if SimulationSettings.SimulationSettings.UseIDPMode:
      """
      Use this ruleset to model IDPs.
      """
      for i in range(0,linklen):
        # calculate (1/D) * P * 2-C
        # D = distance, P = population, C = conflict status (1 for conflict zone).
        C = 0
        if self.location.links[i].endpoint.movechance > 0.5:
          C = 1

        weights[i] = ( 1 / self.location.links[i].distance ) * self.location.links[i].endpoint.pop * (2-C)

    elif not SimulationSettings.SimulationSettings.UseDynamicAwareness:
      for i in range(0,linklen):
        if self.location.links[i].endpoint.getCapMultiplier(self.location.links[i].numAgents) <= 0.000001:
          weights[i] = 0.0
        # forced redirection: if this is true for a link, return its value immediately.
        elif self.location.links[i].forced_redirection == True:
          return i
        else:
          weights[i] = self.getLinkWeight(self.location.links[i], SimulationSettings.SimulationSettings.AwarenessLevel)

          # Throttle down weight when occupancy is close to peak capacity.
          weights[i] *= self.location.links[i].endpoint.getCapMultiplier(self.location.links[i].numAgents)

    else:
      for i in range(0,linklen):
        # forced redirection: if this is true for a link, return its value immediately.
        if self.location.links[i].endpoint.getCapMultiplier(self.location.links[i].numAgents) <= 0.000001:
          weights[i] = 0.0
        elif self.location.links[i].forced_redirection == True:
          return i
        else:
          if self.timesteps_since_departure < 1:
            weights[i] = self.getLinkWeight(self.location.links[i], 0)
          elif self.timesteps_since_departure < 2:
            weights[i] = self.getLinkWeight(self.location.links[i], 1)
          elif self.timesteps_since_departure < 4:
            weights[i] = self.getLinkWeight(self.location.links[i], 2)
          else:
            weights[i] = self.getLinkWeight(self.location.links[i], 3)

          # Throttle down weight when occupancy is close to peak capacity.
          weights[i] *= self.location.links[i].endpoint.getCapMultiplier(self.location.links[i].numAgents)

    if len(weights) == 0:
      return -1
    else:
      if np.sum(weights) > 0.0:
        weights /= np.sum(weights)
      else: # if all have zero weight, then we do equal weighting.
        weights += 1.0/float(len(weights))

      #if len(weights) != len(list(range(0,len(self.location.links)))):
      #  print(weights, list(range(0,len(self.location.links))))

      return np.random.choice(list(range(0,len(self.location.links))), p=weights)

class Location:
  def __init__(self, name, x=0.0, y=0.0, movechance=0.001, capacity=-1, pop=0, foreign=False, country="unknown"):
    self.name = name
    self.x = x
    self.y = y
    self.movechance = movechance
    self.links = [] # paths connecting to other towns
    self.closed_links = [] #paths connecting to other towns that are closed.
    self.numAgents = 0 # refugee population
    self.numAgentsOnRank = 0 # refugee population on current rank (for pflee).
    self.capacity = capacity # refugee capacity
    self.pop = pop # non-refugee population
    self.foreign = foreign
    self.country = country
    self.conflict = False
    self.camp = False
    self.forward = False
    self.time = 0 # keep track of the time in the simulation locally, to build in capacity-related behavior.

    if isinstance(movechance, str):
      if "camp" in movechance.lower():
        self.movechance = SimulationSettings.SimulationSettings.CampMoveChance
        self.camp = True
        self.foreign = True
      elif "conflict" in movechance.lower():
        self.movechance = SimulationSettings.SimulationSettings.ConflictMoveChance
        self.conflict = True
      elif "forward" in movechance.lower():
        self.movechance = 1.0
        self.forward = True
      elif "default" in movechance.lower() or "town" in movechance.lower():
        self.movechance = SimulationSettings.SimulationSettings.DefaultMoveChance
      else:
        print("Error in creating Location() object: cannot parse movechance value of ", movechance, " for location object with name ", name, ".")

    # Automatically tags a location as a Camp if refugees are less than 2% likely to move out on a given day.
    if self.movechance < 0.02 and not self.camp:
      print("Warning: automatically setting location %s to camp, as movechance = %s" % (self.name, self.movechance), file=sys.stderr)
      self.camp = True

    self.LocationScore = 1.0 # Value of Location. Should be between 0.5 and SimulationSettings.SimulationSettings.CampWeight.
    self.NeighbourhoodScore = 1.0 # Value of Neighbourhood. Should be between 0.5 and SimulationSettings.SimulationSettings.CampWeight.
    self.RegionScore = 1.0 # Value of surrounding region. Should be between 0.5 and SimulationSettings.SimulationSettings.CampWeight.
    self.scores = np.array([1.0,1.0,1.0,1.0])

    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      self.incoming_journey_lengths = [] # reinitializes every time step. Contains individual journey lengths from incoming agents.

    self.print()


  def print(self):
    print("Location name: %s, X: %s, Y: %s, movechance: %s, cap: %s, pop: %s, country: %s, conflict? %s, camp? %s" % (self.name, self.x, self.y, self.movechance, self.capacity, self.pop, self.country, self.conflict, self.camp), file=sys.stderr)
    for l in self.links:
      print("Link from %s to %s, dist: %s, pop. %s" % (self.name, l.endpoint.name, l.distance, l.numAgents), file=sys.stderr)

  def SetConflictMoveChance(self):
    """ Modify move chance to the default value set for conflict regions. """
    self.movechance = SimulationSettings.SimulationSettings.ConflictMoveChance

  def SetCampMoveChance(self):
    """ Modify move chance to the default value set for camps. """
    self.movechance = SimulationSettings.SimulationSettings.CampMoveChance


  def CalculateResidualWeightingFactor(self, residual, cap_limit, nearly_full_occ):
    """
    Calculate the residual weighting factor, when pop is between 0.9 and 1.0 of capacity (with default settings).
    Weight should be 1.0 at 0.9, and 0.0 at 1.0 capacity level.
    Asserts are added to prevent corruption of simulation results in case this function misbehaves.
    """

    weight = 1.0 - (residual / (cap_limit * (1.0 - nearly_full_occ)))

    assert(weight >= 0.0)
    assert(weight <= 1.0)

    return weight


  def getCapMultiplier(self, numOnLink):
    """ Checks whether a given location has reached full capacity or is close to it.
        returns 1.0 if occupancy < nearly_full_occ (0.9).
        returns 0.0 if occupancy >= 1.0.
        returns a value in between for intermediate values
    """
    nearly_full_occ = 0.9 #occupancy rate to be considered nearly full.
    cap_limit = self.capacity * SimulationSettings.SimulationSettings.CapacityBuffer #full occupancy limit (should be equal to self.capacity).

    if self.capacity < 0:
      return 1.0
    elif self.numAgents <= nearly_full_occ * cap_limit:
      return 1.0
    elif self.numAgents >= 1.0 * cap_limit:
      return 0.0

    residual = self.numAgents - (nearly_full_occ * cap_limit) # should be a number equal in range [0 to 0.1*self.numAgents].
    
    return self.CalculateResidualWeightingFactor(residual, cap_limit, nearly_full_occ)


  def updateLocationScore(self, time):
    """ Attractiveness of the local point, based on local point information only. """

    self.time = time

    if self.foreign:
      self.LocationScore = SimulationSettings.SimulationSettings.CampWeight
    elif self.conflict:
      self.LocationScore = SimulationSettings.SimulationSettings.ConflictWeight
    else:
      self.LocationScore = 1.0

  def updateNeighbourhoodScore(self):

    """ Attractiveness of the local point, based on information from local and adjacent points, weighted by link length. """
    # No links connected or a Camp? Use LocationScore.
    if len(self.links) == 0 or self.camp:
      self.NeighbourhoodScore = self.LocationScore
      return


    self.NeighbourhoodScore = 0.0
    total_link_weight = 0.0

    for i in self.links:
      self.NeighbourhoodScore += i.endpoint.LocationScore / float(i.distance)
      total_link_weight += 1.0 / float(i.distance)

    self.NeighbourhoodScore /= total_link_weight

  def updateRegionScore(self):
    """ Attractiveness of the local point, based on neighbourhood information from local and adjacent points,
        weighted by link length. """
    # No links connected or a Camp? Use LocationScore.
    if len(self.links) == 0 or self.camp:
      self.RegionScore = self.LocationScore
      return

    self.RegionScore = 0.0
    total_link_weight = 0.0

    for i in self.links:
      self.RegionScore += i.endpoint.NeighbourhoodScore / float(i.distance)
      total_link_weight += 1.0 / float(i.distance)

    self.RegionScore /= total_link_weight
    self.scores = np.array([1.0, self.LocationScore, self.NeighbourhoodScore, self.RegionScore])

class Link:
  def __init__(self, endpoint, distance, forced_redirection=False):
    self.name = "__link__"

    # distance in km.
    self.distance = float(distance)

    # links for now always connect two endpoints
    self.endpoint = endpoint

    # number of agents that are in transit.
    self.numAgents = 0
    self.numAgentsOnRank = 0 # refugee population on current rank (for pflee).

    # if True, then all Persons will go down this link.
    self.forced_redirection = forced_redirection


class Ecosystem:
  def __init__(self):
    self.locations = []
    self.locationNames = []
    self.agents = []
    self.closures = [] #format [type, source, dest, start, end]
    self.time = 0

    # Bring conflict zone management into FLEE.
    self.conflict_zones = []
    self.conflict_zone_names = []
    self.conflict_weights = np.array([])
    self.conflict_pop = 0

    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      self.num_arrivals = [] # one element per time step.
      self.travel_durations = [] # one element per time step.

  def get_camp_names(self):
    camp_names = []
    for l in self.locations:
      if l.camp:
        camp_names += [l.name]
    return camp_names

  def export_graph(self, use_ids_instead_of_names=False):
    vertices = []
    edges = []
    for l in self.locations:
      vertices += [l.name]
      for p in l.links:
        edges += [[l.name, p.endpoint.name, p.distance]]

    return vertices, edges

  def _aggregate_arrivals(self):
    """
    Add up arrival statistics, to find out travel durations and total number of camp arrivals.
    """
    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      arrival_total = 0
      tmp_num_arrivals = 0

      for l in self.locations:
        if l.Camp == True:
          arrival_total += np.sum(l.incoming_journey_lengths)
          tmp_num_arrivals += len(l.incoming_journey_lengths)
          l.incoming_journey_lengths = []

      self.num_arrivals += [tmp_num_arrivals]

      if tmp_num_arrivals>0:
        self.travel_durations += [float(arrival_total) / float(tmp_num_arrivals)]
      else:
        self.travel_durations += [0.0]

      #print("New arrivals: ", self.travel_durations[-1], arrival_total, tmp_num_arrivals)


  def enact_border_closures(self, time, twoway=True):
    #print("Enact border closures: ", self.closures)
    if len(self.closures)>0:
      for c in self.closures:
        if time == c[3]:
          if c[0] == "country":
            print("Time = %s. Closing Border between [%s] and [%s]" % (time, c[1], c[2]), file=sys.stderr)
            self.close_border(c[1],c[2], twoway)
          if c[0] == "location":
            self.close_location(c[1], twoway)
          if c[0] == "link":
            self.close_link(c[1],c[2], twoway)
        if time == c[4]:
          if c[0] == "country":
            print("Time = %s. Reopening Border between [%s] and [%s]" % (time, c[1], c[2]), file=sys.stderr)
            self.reopen_border(c[1],c[2], twoway)
          if c[0] == "location":
            self.reopen_location(c[1], twoway)
          if c[0] == "link":
            self.reopen_link(c[1],c[2], twoway)

  def _convert_location_name_to_index(self, name):
    """
    Convert a location name to an index number
    """
    x = -1
    # Convert name "startpoint" to index "x".
    for i in range(0, len(self.locations)):
      if(self.locations[i].name == name):
        x = i

    if x<0:
      print("#Warning: location not found in remove_link")
      return False

    return x

  def _remove_link_1way(self, startpoint, endpoint, close_only=False):
    """
    Remove link in one direction (private function, use remove_link instead).
    close_only: if True will instead move the link to the closed_links list of the location, rendering it inactive.
    """
    new_links = []
    x = self._convert_location_name_to_index(startpoint)
    removed = False

    for i in range(0, len(self.locations[x].links)):
      if self.locations[x].links[i].endpoint.name is not endpoint:
        new_links += [self.locations[x].links[i]]
        continue
      elif close_only:
        #print("Closing [%s] to [%s]" % (startpoint, endpoint), file=sys.stderr)
        self.locations[x].closed_links += [copy.copy(self.locations[x].links[i])]
      removed = True

    self.locations[x].links = new_links
    if not removed:
      print("Warning: cannot remove link from %s, as there is no link to %s" % (startpoint, endpoint),file=sys.stderr)
    return removed


  def _reopen_link_1way(self, startpoint, endpoint):
    """
    Reopen a closed link.
    """
    new_closed_links = []
    x = self._convert_location_name_to_index(startpoint)
    reopened = False
    #print("Reopening link from %s to %s, closed link list length = %s." % (startpoint, endpoint, len(self.locations[x].closed_links)), file=sys.stderr)

    for i in range(0, len(self.locations[x].closed_links)):
      if self.locations[x].closed_links[i].endpoint.name is not endpoint:
        #print("[%s] to [%s] (%s)" % (startpoint, self.locations[x].closed_links[i].endpoint.name, endpoint), file=sys.stderr)
        new_closed_links += [self.locations[x].closed_links[i]]
      else:
        #print("Match: [%s] to [%s] (%s)" % (startpoint, self.locations[x].closed_links[i].endpoint.name, endpoint), file=sys.stderr)
        self.locations[x].links += [self.locations[x].closed_links[i]]
        reopened = True

    self.locations[x].closed_links = new_closed_links
    if not reopened:
      print("Warning: cannot reopen link from %s, as there is no link to %s" % (startpoint, endpoint),file=sys.stderr)
    return reopened


  def remove_link(self, startpoint, endpoint, twoway=True, close_only=False):
    """
    Removes a link between two location names.
    twoway: if True, also removes link from endpoint to startpoint.
    close_only: if True will instead move the link to the closed_links list of the location, rendering it inactive.
    """
    if twoway:
      self._remove_link_1way(endpoint, startpoint, close_only)
    return self._remove_link_1way(startpoint, endpoint, close_only)


  def reopen_link(self, startpoint, endpoint, twoway=True):
    """
    Reopens a previously closed link between two location names.
    twoway: if True, also removes link from endpoint to startpoint.
    """
    if twoway:
      self._reopen_link_1way(endpoint, startpoint)
    return self._reopen_link_1way(startpoint, endpoint)


  def close_link(self, startpoint, endpoint, twoway=True):
    """
    Shorthand call for remove_link, only moving the link to the closed list.
    """
    return self.remove_link(startpoint, endpoint, twoway=twoway, close_only=True)

  def _change_location_1way(self, location_name, mode="close", direction="both"):
    """
    Close all links to or from one location.
    mode: close or reopen
    direction: in, out or both.
    """

    dir_mode = 0
    if direction == "out":
      dir_mode = 1
    elif direction == "both":
      dir_mode = 2

    print("%s location 1 way [%s] in direction %s (%s)." % (mode, location_name, direction, dir_mode), file=sys.stderr)
    changed_anything = False

    for i in range(0, len(self.locationNames)):
      if self.locationNames[i] == location_name:
        changed_anything = True

        link_set = self.locations[i].links
        if mode == "reopen":
          link_set = self.locations[i].closed_links

        j = 0
        while j < len(link_set):
          print("starting to %s link [%s] [%s] in direction %s" % (mode, location_name, link_set[j].endpoint.name, direction), file=sys.stderr)
          if mode == "close":

            if dir_mode % 2 == 0:
              self.close_link(link_set[j].endpoint.name, self.locationNames[i], twoway=False)

            if dir_mode > 0:
              if self.close_link(self.locationNames[i], link_set[j].endpoint.name, twoway=False):
                link_set = self.locations[i].links # shrink the link list. # This operation affects the overall loop, so no major operations should take place after this.
            else:
              j += 1

          elif mode == "reopen":

            if dir_mode % 2 == 0:
              self.reopen_link(link_set[j].endpoint.name, self.locationNames[i], twoway=False)

            if dir_mode > 0:
              if self.reopen_link(self.locationNames[i], link_set[j].endpoint.name, twoway=False):
                link_set = self.locations[i].closed_links # shrink the closed link list. # This operation affects the overall loop, so no major operations should take place after this.
              else:
                j += 1

    return changed_anything

  def _change_border_1way(self, source_country, dest_country, mode="close"):
    """
    Close all links between two countries in one direction.
    """
    #print("%s border 1 way [%s] [%s]" % (mode, source_country, dest_country), file=sys.stderr)
    changed_anything = False
    for i in range(0, len(self.locationNames)):
      if self.locations[i].country == source_country:

        link_set = self.locations[i].links
        if mode == "reopen":
          link_set = self.locations[i].closed_links

        j = 0
        while j < len(link_set):
          if link_set[j].endpoint.country == dest_country:
            print("starting to %s border 1 way [%s/%s] [%s/%s]" % (mode, source_country, self.locations[i].name, dest_country, link_set[j].endpoint.name), file=sys.stderr)
            changed_anything = True
            if mode == "close":
              if self.close_link(self.locationNames[i], link_set[j].endpoint.name, twoway=False):
                link_set = self.locations[i].links
                continue
            elif mode == "reopen":
              if self.reopen_link(self.locationNames[i], link_set[j].endpoint.name, twoway=False):
                link_set = self.locations[i].closed_links
                continue
          j += 1

    if not changed_anything:
      print("Warning: no link closed when closing borders between %s and %s." % (source_country, dest_country), file=sys.stderr)

  def close_border(self, source_country, dest_country, twoway=True):
    """
    Close all links between two countries. If twoway is set to false, the only links from source to destination will be closed.
    """
    self._change_border_1way(source_country, dest_country, mode="close")
    if twoway:
      self._change_border_1way(dest_country, source_country, mode="close")

  def reopen_border(self, source_country, dest_country, twoway=True):
    """
    Re-open all links between two countries. If twoway is set to false, the only links from source to destination will be closed.
    """
    self._change_border_1way(source_country, dest_country, mode="reopen")
    if twoway:
      self._change_border_1way(dest_country, source_country, mode="reopen")

  def close_location(self, location_name, twoway=True):
    """
    Close in- and outgoing links for a location.
    """
    if twoway:
      return self._change_location_1way(location_name, mode="close", direction="both")
    else:
      return self._change_location_1way(location_name, mode="close", direction="in")

  def reopen_location(self, location_name, twoway=True):
    """
    Reopen in- and outgoing links for a location.
    """
    if twoway:
      self._change_location_1way(location_name, mode="reopen", direction="both")
    else:
      self._change_location_1way(location_name, mode="reopen", direction="in")

  def add_conflict_zone(self, name, change_movechance=True):
    """
    Adds a conflict zone. Default weight is equal to population of the location.
    """
    for i in range(0, len(self.locationNames)):
      if self.locationNames[i] == name:
        if name not in self.conflict_zone_names:
          if change_movechance:
            self.locations[i].movechance = SimulationSettings.SimulationSettings.ConflictMoveChance
            self.locations[i].Conflict = True
          self.conflict_zone_names += [name]
          self.conflict_zones += [self.locations[i]]
          self.conflict_weights = np.append(self.conflict_weights, [self.locations[i].pop])
          self.conflict_pop = sum(self.conflict_weights)
          if SimulationSettings.SimulationSettings.InitLogLevel > 0:
            print("Added conflict zone:", name, ", pop. ", self.locations[i].pop)
            print("New total pop. in conflict zones: ", self.conflict_pop)
          return

    print("Diagnostic: self.locationNames: ", self.locationNames)
    print("ERROR in flee.add_conflict_zone: location with name [%s] appears not to exist in the FLEE ecosystem (see diagnostic above)." % (name))


  def remove_conflict_zone(self, name):
    """
    Shorthand function to remove a conflict zone from the list.
    (not used yet)
    """
    new_conflict_zones = []
    new_conflict_zone_names = []
    new_weights = np.array([])

    for i in range(0, len(self.conflict_zones)):
      if conflict_zones[i].name is not name:
        new_conflict_zones += [self.conflict_zones[i]]
        new_conflict_zone_names += [self.conflict_zone_names[i]]
        new_weights = np.append(new_weights, [self.conflict_weights[i]])

    self.conflict_zones = new_conflict_zones
    self.conflict_weights =  new_weights
    self.conflict_pop = sum(self.conflict_weights)


  def pick_conflict_location(self):
    """
    Returns a weighted random element from the list of conflict locations.
    This function returns a number, which is an index in the array of conflict locations.
    """
    return np.random.choice(self.conflict_zones, p=self.conflict_weights/self.conflict_pop)


  def refresh_conflict_weights(self):
    """
    This function needs to be called when SimulationSettings.SimulationSettings.TakeRefugeesFromPopulation is set to True.
    It will update the weights to reflect the new population numbers.
    """
    for i in range(0,len(self.conflict_zones)):
      self.conflict_weights[i] = self.conflict_zones[i].pop
    self.conflict_pop = sum(self.conflict_weights)

  def evolve(self):
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

    for a in self.agents:
      a.finish_travel()

    #update link properties
    if SimulationSettings.SimulationSettings.CampLogLevel > 0:
      self._aggregate_arrivals()
    self.time += 1

  def addLocation(self, name, x="0.0", y="0.0", movechance=SimulationSettings.SimulationSettings.DefaultMoveChance, capacity=-1, pop=0, foreign=False, country="unknown"):
    """ Add a location to the ABM network graph """

    l = Location(name, x, y, movechance, capacity, pop, foreign, country)
    if SimulationSettings.SimulationSettings.InitLogLevel > 0:
      print("Location:", name, x, y, l.movechance, capacity, ", pop. ", pop, foreign)
    self.locations.append(l)
    self.locationNames.append(l.name)
    return l


  def addAgent(self, location):
    if SimulationSettings.SimulationSettings.TakeRefugeesFromPopulation:
      if location.pop > 0:
        location.pop -= 1
    self.agents.append(Person(location))

  def insertAgent(self, location):
    """
    Note: insert Agent does NOT take from Population.
    """
    self.agents.append(Person(location))

  def insertAgents(self, location, number):
    for i in range(0,number):
      self.insertAgent(location)

  def clearLocationsFromAgents(self, location_names):
    """
    Remove all agents from a list of locations by name.
    Useful for couplings to other simulation codes.
    """

    new_agents = []
    for i in range(0, len(self.agents)):
      if self.agents[i].location.name not in location_names:
        new_agents += agents[i] #agent is preserved in ecosystem.
      else:
        self.agents[i].location.numAgents -= 1 #agent is removed from exosystem and number of agents in location drops by one.
    self.agents = new_agents

  def numAgents(self):
    return len(self.agents)


  def linkUp(self, endpoint1, endpoint2, distance="1.0", forced_redirection=False):
    """ Creates a link between two endpoint locations
    """
    endpoint1_index = -1
    endpoint2_index = -1
    for i in range(0, len(self.locationNames)):
      if(self.locationNames[i] == endpoint1):
        endpoint1_index = i
      if(self.locationNames[i] == endpoint2):
        endpoint2_index = i

    if endpoint1_index < 0:
      print("Diagnostic: Ecosystem.locationNames: ", self.locationNames)
      print("Error: link created to non-existent source: ", endpoint1, " with dest ", endpoint2)
      sys.exit()
    if endpoint2_index < 0:
      print("Diagnostic: Ecosystem.locationNames: ", self.locationNames)
      print("Error: link created to non-existent destination: ", endpoint2, " with source ", endpoint1)
      sys.exit()

    self.locations[endpoint1_index].links.append( Link(self.locations[endpoint2_index], distance, forced_redirection) )
    self.locations[endpoint2_index].links.append( Link(self.locations[endpoint1_index], distance) )

  def printInfo(self):
    print("Time: ", self.time, ", # of agents: ", len(self.agents))
    for l in self.locations:
      print(l.name, l.numAgents, file=sys.stderr)

  def printComplete(self):
    print("Time: ", self.time, ", # of agents: ", len(self.agents))
    for l in self.locations:
      print("Location name %s, number of agents %s" % (l.name, l.numAgents), file=sys.stderr)
      l.print()


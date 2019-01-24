# coupling.py
# File which contains the multiscale coupling interface for FLEE.
# Idea is to support a wide range of coupling mechanisms within this Python file.
import os.path
import time
import csv
import sys

class CouplingInterface:

  def __init__(self, e, coupling_type="file"):
    """ Constructor.
    e = FLEE ecosystem
    Coupling types to support eventually:
        - file
        - MPWide
        - one-sided store
        - repository coupling.
        - muscle
    """
    self.coupling_type = coupling_type

    # coupling definitions.
    self.e = e
    self.location_ids = []
    self.location_names = []
    self.names = []
    self.directions = []
    self.intervals = []

    if coupling_type=="muscle":
      import muscle
      muscle.init() #add sys.argv?

  def addCoupledLocation(self, location, name, direction="inout", interval=1):
    """
    Adds a locations to the so-called *Coupled Region*.
    * Location is the (p)Flee location object.
    * Name is a location identifier that is identical to the one in the other code.
    * Direction can be (once the code is done):
      - "out" -> agents are removed and stored in the coupling link.
      - "in" -> agents written to the coupling link by the other process are added to this location.
      - "inout" -> both out and in.
      - "inout indirect" -> changes in agent numbers are stored in the coupling link. No agents are added or removed.
    * Interval is the timestep interval of the coupling, ensuring that the coupling activity is performed every <interval> time steps.
    """
    self.location_ids += [self.e._convert_location_name_to_index(location.name)]
    self.location_names += [location.name]
    self.names += [name]
    self.directions += [direction]
    self.intervals += [interval]
    self.coupling_rank = True
    if self.e.mpi != None:
      if self.e.mpi.rank > 0:
        self.coupling_rank = False

  def Couple(self, t): #TODO: make this code more dynamic/flexible
    newAgents = None
    if t % self.intervals[0] == 0: #for the time being all intervals will have to be the same...
      if self.coupling_type=="muscle":
        if self.coupling_rank: #If MPI is used, this will be the process with rank 0
          muscle.send(self.generateOutputCSVString(t), "out", muscle.string)
          newAgents = self.extractNewAgentsFromCSVString(muscle.receive("in", muscle.string))

        if self.e.mpi != None: #If MPI is used, broadcast newAgents to all other processes
          newAgents = self.e.mpi.comm.bcast(newAgents, root=0)

      else: #default is coupling through file IO.
        if self.coupling_rank: #If MPI is used, this will be the process with rank 0
          self.writeOutputToFile(t)

        newAgents = self.readInputFromFile(t)

      self.e.clearLocationsFromAgents(self.location_names) #TODO: make this conditional on coupling type.
      for i in range(0, len(self.location_names)):
        #write departing agents to file
        #read incoming agents from file
        #print(self.names, i, newAgents)
        print("Couple IN: %s %s" % (self.names[i], newAgents[self.names[i]]), file=sys.stderr)
        if self.names[i] in newAgents:
          self.e.insertAgents(self.e.locations[self.location_ids[i]], newAgents[self.names[i]])
        self.e.updateNumAgents()

  # File coupling code

  def setCouplingFilenames(self, outputfilename, inputfilename):
    """
    Sets the coupling output file name (for file coupling). Name should be WITHOUT .csv extension.
    """
    self.outputfilename = outputfilename
    self.inputfilename = inputfilename

  def generateOutputCSVString(self, t):
    out_csv_string = ""
    for i in range(0, len(self.location_ids)):
      out_csv_string += "%s,%s\n" % (self.names[i], self.e.locations[self.location_ids[i]].numAgents)
      print("Couple OUT: %s %s" % (self.names[i], self.e.locations[self.location_ids[i]].numAgents), file=sys.stderr)
    return out_csv_string

  def writeOutputToFile(self, t):
    out_csv_string = self.generateOutputCSVString(t)
    with open('%s.%s.csv' % (self.outputfilename, t),'a') as file:
      file.write(out_csv_string)

    print("Couple: output written to %s.%s.csv" % (self.outputfilename, t), file=sys.stderr)

  def extractNewAgentsFromCSVString(self, csv_string):
    """
    Reads in a CSV string with coupling information, and extracts a list of New Agents.
    """
    newAgents = {}

    for line in csv_string:
      row = line.split(',')
      if len(row[0]) == 0:
        continue
      if row[0][0] == "#":
        pass
      else:
        for i in range(0, len(self.location_ids)):
          if row[0] == self.names[i]:
            newAgents[self.names[i]] = int(row[1])
    return newAgents

  def readInputFromFile(self, t):
    """
    Returns a dictionary with key <coupling name> and value <number of agents>.
    """
    in_fname = "%s.%s.csv" % (self.inputfilename, t)

    print("Couple: searching for", in_fname, file=sys.stderr)
    while not os.path.exists(in_fname):
      time.sleep(0.1)
    time.sleep(0.001)

    csv_string = ""
    with open("%s.%s.csv" % (self.inputfilename, t)) as csvfile:
      csv_string = csvfile.read().split('\n')

    return self.extractNewAgentsFromCSVString(csv_string)

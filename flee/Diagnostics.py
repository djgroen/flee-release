def write_agents(agents, time, max_written=-1, timestep_interval=1):
    """
    Write agent data to file. Write only up to <max_written> agents each time step, and only write a file every <timestep_interval> time steps.
    """

    my_file = open('agents.out.%s' % time, 'w', encoding='utf-8')

    if max_written < 0:
        max_written = len(agents)

    print("# current location, location of origin, is travelling, distance travelled, places travelled.", file=my_file)

    for k,a in enumerate(agents[0:max_written]):
        if k % timestep_interval == 0:
            print("{},{},{},{},{}".format(a.location.name,a.home_location.name,a.travelling,a.distance_travelled,a.places_travelled), file=my_file)



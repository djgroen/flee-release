


import math
import csv
import os
import pandas as pd
import numpy as np


def distance_on_unit_sphere(lat1, long1, lat2, long2):
    #https://gist.github.com/matbor/6837804
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math. pi /180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1 ) *degrees_to_radians
    phi2 = (90.0 - lat2 ) *degrees_to_radians

    # theta = longitude
    theta1 = long1* degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) =
    # sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc * 6371

def get_capital_gps_location(path_locations_file, district):
    loc = pd.read_csv(path_locations_file, header=0, index_col=0, skipinitialspace=True)
    return loc['gps x'][district], loc['gps y'][district]

def update_links(path_links_file, path_locations_file):
    #links_file = open(path_links_file, "r")
    #locations_file = open(path_locations_file, "r")
    path_out_file = os.path.splitext(path_links_file)[0] + '-dist.csv'
    fileout = open(path_out_file, "w")
    fileout.write('#location1,location2,gps distance (km)\n')
    #csvrdr = csv.reader(links_file, delimiter=",")
    with open(path_links_file, "r") as links_file:
        csvrdr_links = csv.DictReader(links_file)
        for row in csvrdr_links:
            lat1, long1 = get_capital_gps_location(path_locations_file, row['#location1'])
            lat2, long2 = get_capital_gps_location(path_locations_file, row['location2'])
            dist_temp = distance_on_unit_sphere(lat1, long1, lat2, long2)
            #print(row['#location1'], row['location2'], str(dist_temp))
            fileout.write(row['#location1'] + ',' + row['location2'] + ',' + str(int(np.round(dist_temp))) + '\n')
    fileout.close()


if __name__ == "__main__":
    path_links_file = 'iraq/iraq-links.csv'
    path_locations_file = 'iraq/iraq-locations.csv'
    update_links(path_links_file, path_locations_file)

# Requests data from the mtn project API.
import os
import yaml
import requests
import json

# Uncomment the area to grab its routes
# Overlap may mean filtering for uniques later

#datafilename = "foster-falls"
#LAT = "35.182"
#LON = "-85.674"
#RADIUS = 3 #(In miles. I'm assuming this uses haversine distance)

# datafilename = "t-wall"
# LAT = "35.072"
# LON = "-85.403"
# RADIUS = 3

# datafilename = "sunset"
# LAT = "34.999"
# LON = "-85.355"
# RADIUS = 3

# datafilename = "little-rock-city"
# LAT = "35.248"
# LON = "-85.221"
# RADIUS = 3

datafilename = "deep-creek"
LAT = "35.296"
LON = "-85.195"
RADIUS = 2

# More areas to be included in the future, incl. bama, kentucky, NC

def load_yaml_creds(filename=None):
    """Reads my private key from a YAML file.

       Returns:
       string: parsed private key
    """
    try:
        with open(os.path.expanduser(filename)) as file:
            pkey = yaml.safe_load(file)
    except FileNotFoundError:
        print("Cannot find file {}".format(filename))
        pkey = {}

    return pkey

def build_request():
    """Pieces together the request from its parameters.

       Returns:
       String: url with which to make API request OR empy dict if no key was found
    """
    baseurl = "https://www.mountainproject.com/data/get-routes-for-lat-lon?"
    lat = LAT
    lon = LON
    maxDistance = RADIUS
    maxResults = 500
    pkey = load_yaml_creds("~/request-routes/.mp-pkey.yaml")
    if pkey=={}:
        print("no key found")
        return {}
    return "{}lat={}&lon={}&maxDistance={}&maxResults={}&key={}".format(baseurl, lat, lon, maxDistance, maxResults, pkey)

def make_request():
    req = build_request()
    resp = requests.get(req)
    with open('{}.JSON'.format(datafilename), 'w') as response_file:
        json.dump(resp.json(), response_file, indent=4)

make_request()
# The url should look like this example:
# "https://www.mountainproject.com/data/get-routes-for-lat-lon?lat=40.03&lon=-105.25&maxDistance=10&minDiff=5.6&maxDiff=5.10&key=$YOURKEY

# Required Arguments:
# key - Your private key
# lat - Latitude for a given area
# lon - Longitude for a given area

# Optional Arguments:
# maxDistance - Max distance, in miles, from lat, lon. Default: 30. Max: 200.
# maxResults - Max number of routes to return. Default: 50. Max: 500.
# minDiff - Min difficulty of routes to return, e.g. 5.6 or V0.
# maxDiff - Max difficulty of routes to return, e.g. 5.10a or V2.

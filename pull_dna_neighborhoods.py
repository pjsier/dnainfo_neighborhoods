import subprocess
import json
import re
import os
from functools import partial
from multiprocessing.dummy import Pool

# Declare empty lists and dicts for subprocess calls, geojson, and errors
calls = []
neighb_dict = {}
errors = []
geoj_features = {
    "type": "FeatureCollection",
    "features": []
}

# List from DNAInfo
neighborhoods = [
    'bucktown',
    'garfield-park',
    'norwood-park',
    'canaryville',
    'gladstone-park',
    'mckinley-park',
    'sauganash',
    'west-beverly',
    'montclare',
    'marquette-park',
    'river-west',
    'west-pullman',
    'lakeview',
    'old-irving-park',
    'south-loop',
    'bronzeville',
    'noble-square',
    'uptown',
    'west-humboldt-park',
    'albany-park',
    'pullman',
    'burnside',
    'jefferson-park',
    'ravenswood-gardens',
    'west-lawn',
    'gold-coast',
    'mayfair',
    'chicago-lawn',
    'kenwood',
    'edison-park',
    'ukrainian-village',
    'greektown',
    'bush',
    'grand-crossing',
    'river-north',
    'oakland',
    'back-of-yards',
    'washington-park',
    'avalon-park',
    'ravenswood-manor',
    'independence-park',
    'east-garfield-park',
    'gap',
    'ashburn',
    'wrigleyville',
    'south-austin',
    'pilsen',
    'lincoln-square',
    'avondale',
    'north-lawndale',
    'auburn-gresham',
    'east-side',
    'south-deering',
    'garfield-ridge',
    'englewood',
    'tri-taylor',
    'ravenswood',
    'bridgeport',
    'logan-square',
    'chinatown',
    'old-edgebrook',
    'ford-city',
    'armour-square',
    'mt-greenwood',
    'beverly',
    'university-village',
    'rogers-park',
    'north-park',
    'morgan-park',
    'loop',
    'humboldt-park',
    'near-west-side',
    'hyde-park',
    'north-edgebrook',
    'little-italy',
    'brainerd',
    'belmont-cragin',
    'fuller-park',
    'west-town',
    'irving-park',
    'dunning',
    'buena-park',
    'edgewater',
    'west-englewood',
    'gage-park',
    'heart-of-italy',
    'west-elsdon',
    'medical-district',
    'roseland',
    'boystown',
    'clearing',
    'andersonville',
    'east-village',
    'douglas',
    'roscoe-village',
    'south-lawndale',
    'galewood',
    'forest-glen',
    'calumet-heights',
    'south-chicago',
    'altgeld-gardens',
    'hermosa',
    'west-ridge',
    'archer-heights',
    'edgebrook',
    'streeterville',
    'hegewisch',
    'west-rogers-park',
    'pill-hill',
    'portage-park',
    'heart-of-chicago',
    'grand-boulevard',
    'wicker-park',
    'new-city',
    'lincoln-park',
    'chatham',
    'south-shore',
    'downtown',
    'woodlawn',
    'little-village',
    'washington-heights',
    'brighton-park',
    'old-town',
    'north-center',
    'jackson-highlands',
    'ohare',
    'riverdale',
    'austin',
    'midway',
    'west-loop'
]

stops_query = "getstopsbyrouteanddirection&routeid={0}&d={1}"

dna_base_url = "https://visualizations.dnainfo.com/"
topo_url = dna_base_url + "static/crimemaps/neigh_drawn_geojsons/chi-{0}/polys_chi{1}_25.topojson"
geo_url = dna_base_url + "getallchidrawngeojson/{0}/0/"

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

def clean_geojson(neighb):
    with open("data/{0}/{0}.geojson".format(neighb), 'r+') as gf:
        geo_new = json.load(gf)
        # After reading file in, return to beginning and truncate
        gf.seek(0)
        gf.truncate()
        # Some have strange empty strings, filter those out
        geo_write = [json.loads(g) for g in geo_new if g != ""]

        neighb_features = {
            "type": "FeatureCollection",
            "features": []
        }

        for g in geo_write:
            g["properties"]["neighborhood"] = neighb
            # Add to overall list of GeoJSON features, write to file
            geoj_features["features"].append(g)
            neighb_features["features"].append(g)

        gf.write(json.dumps(neighb_features))

# Check if path isn't already created, otherwise create directories and topojson
for neighb in neighborhoods:
    if not os.path.exists(BASE_DIR + "/data/{0}".format(neighb)):
        subprocess.call(["mkdir", "-p", "data/{0}".format(neighb)])
        # Remove any hyphens to match topojson file naming conventions
        rn = re.sub('[^a-z]+', '', neighb)

        topo_call = topo_url.format(neighb, rn)
        geo_call = geo_url.format(neighb)
        wget_topo = "wget -O data/{0}/{0}.topojson {1}".format(neighb, topo_call)
        wget_geo = "wget -O data/{0}/{0}.geojson {1}".format(neighb, geo_call)

        calls.extend((wget_topo, wget_geo))

# Run wget calls for GeoJSON in multiple processes to speed up
pool = Pool(4)
for i, returncode in enumerate(pool.imap(partial(subprocess.call, shell=True), calls)):
    if returncode != 0:
       errors.append(calls[i])

# List comprehension to clean all GeoJSON files and create master file
[clean_geojson(n) for n in neighborhoods]

with open("dna_neighborhoods.geojson", "w") as gf:
    gf.write(json.dumps(geoj_features))

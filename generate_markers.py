import csv
import json
import os
import glob
from collections import defaultdict

geojson_file = "onlyVAcounties.json"
output_dir = "output"
output_markers_file = "markers.json"
permaMarkers_dir = "permaMarkers.json"
SeenAccidents_file = "SeenAccidents.json"


def get_latest_csv(directory):
    list_of_files = glob.glob(f"{directory}/*.csv")
    if not list_of_files:
        raise FileNotFoundError("Ruh ro")
    return max(list_of_files, key=os.path.getctime)


with open(geojson_file, 'r', encoding='utf-8') as f:
    counties_data = json.load(f)

with open(SeenAccidents_file, 'r', encoding='utf-8') as f:
    seen_accidents = set(json.load(f))


def find_jurisdiction(jurisdiction, geojson_data):
    for feature in geojson_data['features']:
        if jurisdiction.lower() in feature['properties']['NAME'].lower():
            return feature
    return None


csv_file = get_latest_csv(output_dir)

county_accidents = defaultdict(lambda: {"count": 0, "reasons": set()})

new_incidents = 0
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        unique_id = f"{row['Update Time']}|{row['Jurisdiction']}|{row['Route']}|{row['MRM']}|{row['Description']}"
        if unique_id in seen_accidents:
            continue

        seen_accidents.add(unique_id)
        new_incidents += 1

        
        jurisdiction = row['Jurisdiction'].split(" (")[0]

        result = find_jurisdiction(jurisdiction, counties_data)
        if result:
            latitude = result['properties']['latitude']
            longitude = result['properties']['longitude']
            label = row['Label'].split(" - ")[-1]

            county_key = (latitude, longitude)
            county_accidents[county_key]["count"] += 1
            county_accidents[county_key]["reasons"].add(label)
        else:
            pass

with open(SeenAccidents_file, 'w', encoding='utf-8') as f: #Will I remember to add this to the git add workflow?
    json.dump(list(seen_accidents), f)

markers = []

for (latitude, longitude), data in county_accidents.items():
    marker = {
        "latitude": latitude,
        "longitude": longitude,
        "count": data["count"],
        "reasons": list(data["reasons"])
    }
    markers.append(marker)

with open(output_markers_file, 'w', encoding='utf-8') as f:
    json.dump(markers, f, indent=2)


with open(permaMarkers_dir, 'r', encoding='utf-8') as f:
    permamarkersMarkers = json.load(f)


permamarkersMarkers.extend(markers)

unique_markers = {}
for marker in permamarkersMarkers:
    key = (marker["latitude"], marker["longitude"])
    if key in unique_markers:
        unique_markers[key]["count"] += marker["count"]
        unique_markers[key]["reasons"] = list(set(unique_markers[key]["reasons"]) | set(marker["reasons"]))
    else:
        unique_markers[key] = marker

with open(permaMarkers_dir, 'w', encoding='utf-8') as f: # IT WASNT WORKING BECAUSE I FORGOT TO ADD IT TO COMMIT !!!!!!!!
    json.dump(list(unique_markers.values()), f, indent=2)

import csv
import json
import os
import glob

geojson_file = "onlyVAcounties.json"
output_dir = "output"
output_markers_file = "markers.json"

def get_latest_csv(directory):
    list_of_files = glob.glob(f"{directory}/*.csv")
    if not list_of_files:
        raise FileNotFoundError("Empty")
    return max(list_of_files, key=os.path.getctime)

with open(geojson_file, 'r', encoding='utf-8') as f:
    counties_data = json.load(f)

def find_jurisdiction(jurisdiction, geojson_data):
    for feature in geojson_data['features']:
        if jurisdiction.lower() in feature['properties']['NAME'].lower():
            return feature
    return None

csv_file = get_latest_csv(output_dir)

markers = []
with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        jurisdiction = row['Jurisdiction'].split(" (")[0]
        print(f"Processing jurisdiction: {jurisdiction}")

        result = find_jurisdiction(jurisdiction, counties_data)
        if result:
            latitude = result['properties']['latitude']
            longitude = result['properties']['longitude']
            marker = {
                "latitude": latitude,
                "longitude": longitude
            }
            markers.append(marker)
            print(f"Added marker: {marker}")
        else:
            print(f"Jurisdiction not found: {jurisdiction}")

with open(output_markers_file, 'w', encoding='utf-8') as f:
    json.dump(markers, f, indent=2)

print(f"Markers saved to {output_markers_file}")

import json

with open('inverted_index.json') as wil_file:
    data = json.load(wil_file)

results = {}
counter = 0
for key in data:
  results[key] = [x[0] for x in data[key]]

with open('new_inverted_index.json', 'w') as wil_file:\
    json.dump(results, wil_file)

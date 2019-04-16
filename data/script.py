import json

with open('inverted_index.json') as wil_file:
    data = json.load(wil_file)

with open('new_inverted_index.json', 'w') as wil_file:
    json.dump(data["southward"], wil_file)

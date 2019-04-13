import json
import requests
import yaml
import ast
import urllib

with open("./data/name_id_lookup.json", "r") as f:
    name_ids = json.load(f)
    results = {}

    for key in name_ids:
        new_key = key.replace("'","%27")
        new_key = urllib.parse.urlencode({'q':key})

        url = "https://api.pushshift.io/reddit/search/comment/?&subreddit=travel&fields=score,body&sort_type=score&size=50"
        api = requests.get(url, new_key)
        api_call = api.content.decode('utf8').replace("''", '""')
        api_call = ast.literal_eval(api_call)
        results[key] = api_call["data"]
        break

with open("./data/reddit.json", "w") as f:
     json.dump(results, f)

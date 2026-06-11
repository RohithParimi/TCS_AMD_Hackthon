import json
d = json.load(open("data/results.json"))
print(d["meta"])
for e in d["errors"]: print(e["app_name"], "->", e["error"][:200])
import json

objekt = '{"zuletzt online": "heute", "rang": "premium"}'

js = json.loads(objekt)
js["iq"] = 2

objekt = json.dumps(js)

print(objekt)
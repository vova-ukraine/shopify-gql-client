import json

schema = json.load(open("./schema.json"))

types = schema["data"]["__schema"]["types"]

query_root = [t for t in types if t["name"] == "QueryRoot"][0]

# Extract only query names
queries = [f["name"] for f in query_root["fields"]]

# Print evety name in new lines
print("\n".join(queries))

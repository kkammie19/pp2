import json

with open("sample-data.json") as f:
    data = json.load(f)

fmt = "{:50} {:20}  {:6}  {:6}"

print("Interface Status")
print("=" * 80)
print(fmt.format("DN", "Description", "Speed", "MTU"))
print(fmt.format("-" * 50, "-" * 20, "-" * 6, "-" * 6))

for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    print(fmt.format(attrs["dn"], attrs["descr"], attrs["speed"], attrs["mtu"]))
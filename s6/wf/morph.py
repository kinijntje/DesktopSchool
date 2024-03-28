import json

def makeDescription(entries):
    res = ""
    for entry in entries:
        if type(entry) != str and entry['type'] == "entries":
            print(entry['type'])
            descr = makeDescription(entry['entries'])
            res += f"\n\n{entry['name']}\n{descr}"
        elif type(entry) == str:
            res += entry
    return res
        
  
# Opening JSON file
f = open('og_spells.json')
data = json.load(f)

for i in data['spell']:
    school = i["school"]
    nschool = ""
    match school:
        case "A":
            nschool = "Abjuration"
        case "C":
            nschool = "Conjuration"
        case "D":
            nschool = "Divination"
        case "E":
            nschool = "Enchantment"
        case "V":
            nschool = "Evocation"
        case "I":
            nschool = "Illusion"
        case "N":
            nschool = "Necromancy"
        case "T":
            nschool = "Transmutation"
    new = {}
    print(i['name'])
    new['name'] = i['name']
    new['level'] = i['level']
    new['school'] = nschool
    new['timeNumber'] = i['time'][0]['number']
    new['timeUnit'] = i['time'][0]['unit']
    new['description'] = makeDescription(i['entries'])
    
    new["v"] = i["components"]["v"] if "v" in i["components"].keys() else False
    new["s"] = i["components"]["s"] if "s" in i["components"].keys() else False
    new["m"] = i["components"]["m"] if "m" in i["components"].keys() else None
    
    new["rangeType"] = i["range"]["type"]
    new["distanceType"] = i["range"]["distance"]["type"] if new["rangeType"] != "special" else None
    new["distanceAmount"] = i["range"]["distance"]["amount"] if new["distanceType"] == "feet" else None
    
    new["durationUnit"] = i["duration"][0]["type"]
    if new["durationUnit"] == "timed":
        new["durationUnit"] = i["duration"][0]["duration"]["type"]
        new["durationNumber"] = i["duration"][0]["duration"]["amount"]
    
    if "damageInflict" in i.keys():
        new["damageType"] = ",".join(i["damageInflict"])
    else:
        new["damageType"] = None
        
    if "savingThrow" in i.keys():
        new["savingThrow"] = ",".join(i["savingThrow"])
    else:
        new["savingThrow"] = None
        
    if "concentration" in i["duration"][0].keys():
        new["concentration"] = True
    else:
        new["concentration"] = False
    print(new)
    
  
# Closing file
f.close()


    

# {
#   name: ,  String
#   level: , Int
#   school: ,  String
#   timeNumber: ,  Int
#   timeUnit: ,  String (minutes, action, reaction)
#   description: ,  String
#   components: , String ('v,s,m')
#   rangeType: ,  String
#   distanceType: , String (feet, touch, self)
#   distanceAmount: , Int
#   durationNumber: , Int
#   durationUnit: , String (minutes, hours, days)
#   damageType: , String (acid, thunder, ...)
#   savingThrow: , String (dex, con)
#   concentration: , Boolean
# }
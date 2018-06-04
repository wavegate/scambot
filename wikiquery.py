import requests
import json
import re

headers = {
    'authority': 'pathofexile.gamepedia.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'referer': 'https://www.reddit.com/r/pathofexiledev/comments/8a9fgg/poe_wiki_data_retrieval/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.1781378339.1525491837; cdmabp=true; cdmblk=0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0; device_id=2e1bbaa1648b409cab6ab88292d143d1; _ga=GA1.3.1781378339.1525491837; cdmtlk=0:0:0:0:0:0:0:0:0:0:0:0:0:0; cdmgeo=us; cdmbaserate=2.1; cdmbaseraterow=1.1; cdmblk2=0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0:0; cdmu=1526489224800; _gid=GA1.2.648042260.1526974781; _gid=GA1.3.648042260.1526974781; cdmint=0; AWSELB=454155A308F76C609E151FBDFDA83119B9C532839C3103CA42133F7E351EB09D09BBF0E28A42275F6CB6DCB3375014BCEB7F82D529378BD36C40EEB773F0955919B4D38DBB; _gat_tracker0=1; _gat_tracker1=1',
}

params = (
    ('action', 'cargoquery'),
    ('tables', 'items'),
    ('fields', 'name,explicit_mods'),
    ('where', ['rarity="Unique"', 'class="Daggers"']),
    ('limit', '500'),
    ('group_by', ['name']),
    ('format', 'json'),
)

params2 = (
    ('action', 'cargoquery'),
    ('tables', 'mods'),
    ('fields', 'id,stat_text'),
    ('where', ['id="MovementVelocityPenaltyHeavyArmourImplicit"']),
    ('limit', '500'),
    ('group_by', ['id']),
    ('format', 'json'),
)

items = []

filename = "SAVE.txt"
file = open(filename, "a+")

response = requests.get('https://pathofexile.gamepedia.com/api.php', headers=headers, params=params)
data = json.loads(response.text)
for item in data['cargoquery']:
    item['title']['explicit mods'] = item['title']['explicit mods'].split(',')
    items.append(item['title'])

for item in items:
    #file.write(str(item))
    mods = []
    for mod in item['explicit mods']:
        file.write(mod)
        stat_min = None
        stat_max = None
        modParams = (
            ('action', 'cargoquery'),
            ('tables', 'mods'),
            ('fields', 'stat_text'),
            ('where', ['id="' + mod + '"']),
            ('limit', '500'),
            ('group_by', ['id']),
            ('format', 'json'),
        )
        modResponse = requests.get('https://pathofexile.gamepedia.com/api.php', headers=headers, params=modParams)
        modData = json.loads(modResponse.text)
        text = None
        for md in modData['cargoquery']:
            text = md['title']['stat text']
        if text:
            match = re.findall("(\w+-\w+)", text)
            if match:
                if len(match) == 1:
                    numbers = re.search("(\w+)-(\w+)", match[0])
                    stat_min = numbers.group(1)
                    stat_max = numbers.group(2)
                    file.write(stat_min + " " + stat_max)
                #if len(match) == 2:
                #    numbers1 = re.search("(\w+)-(\w+)", match[0])
                #    numbers2 = re.search("(\w+)-(\w+)", match[1])
                #    stat_min = (numbers1.group(1) + numbers1.group(2))/2
    print(mods)

#Adds (50-60) to (120-140) [[Physical Damage]]

#filename = "wikiquery.txt"
#file = open(filename, "w")
#file.write(json.dumps(data, sort_keys=True, indent=4))
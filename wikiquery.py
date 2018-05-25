import requests
import json

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
    ('fields', 'name,class,mods'),
    ('where', ['rarity="Unique"', 'class="Body Armours"']),
    ('limit', '500'),
    ('group_by', ['name']),
    ('format', 'json'),
)

response = requests.get('https://pathofexile.gamepedia.com/api.php', headers=headers, params=params)
data = json.loads(response.text)
for item in data['cargoquery']:
    print(item['title'])
#print(json.dumps(data, sort_keys=True, indent=4))

filename = "wikiquery.txt"
file = open(filename, "w")
file.write(json.dumps(data, sort_keys=True, indent=4))

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://pathofexile.gamepedia.com/api.php?action=cargoquery&tables=items&fields=name,class&where=rarity=%22Unique%22&where=class=%22Jewel%22&limit=5&group_by=name', headers=headers)

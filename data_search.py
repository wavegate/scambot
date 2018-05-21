import requests
from requests_html import HTMLSession
import re

import webbrowser

rates_data = requests.get("http://poe.ninja/api/Data/GetCurrencyOverview?league=Bestiary").json()
parsed_rates_data = {}

UNIQUE_FLASK_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueFlaskOverview?league=Bestiary"
CARD_PRICES_URL = "http://poe.ninja/api/Data/GetDivinationCardsOverview?league=Bestiary"
PROPHECY_PRICES_URL = "http://poe.ninja/api/Data/GetProphecyOverview?league=Bestiary"
UNIQUE_ARMOUR_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueArmourOverview?league=Bestiary"
UNIQUE_WEAPON_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueWeaponOverview?league=Bestiary"
UNIQUE_MAP_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueMapOverview?league=Bestiary"
UNIQUE_ACESSORY_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=Bestiary"
UNIQUE_JEWEL_PRICES_URL = "http://poe.ninja/api/Data/GetUniqueJewelOverview?league=Bestiary"
ESSENCE_OVERVIEW_URL = "http://poe.ninja/api/Data/GetEssenceOverview?league=Bestiary"
CURRENCY_PRICES_URL = "http://poe.ninja/api/Data/GetCurrencyOverview?league=Bestiary"

CURRENCY_FULL = ['Orb of Alteration', 'Orb of Fusing',
                 'Orb of Alchemy', 'Chaos Orb',
                 'Gemcutter\'s Prism', 'Exalted Orb',
                 'Chromatic Orb', 'Jeweller\'s Orb',
                 'Orb of Chance', 'Cartographer\'s Chisel',
                 'Orb of Scouring', 'Blessed Orb',
                 'Orb of Regret', 'Regal Orb', 'Divine Orb',
                 'Vaal Orb']

if rates_data:
    for currency_data in rates_data['lines']:
        if currency_data['currencyTypeName'] in CURRENCY_FULL:
            parsed_rates_data[currency_data['currencyTypeName']] = currency_data['chaosEquivalent']


armor_data = requests.get(UNIQUE_ARMOUR_PRICES_URL).json()
#file = open('jsonviewer.txt', 'w', encoding='utf-8')
#file.write(str(armor_data))
#file.close()
armor_values = {}
if armor_data:
	for unique_data in armor_data['lines']:
		armor_values[unique_data['name']] = unique_data['chaosValue']

data = {
	"league" : "Bestiary",
	"name" : "Victario's Influence"
}

headers = {
	"Connection" : "keep-alive",
	"Cache-Control" : "max-age=0",
	"Origin" : "http://poe.trade",
	"Upgrade-Insecure-Requests" : "1",
	"Content-Type" : "application/x-www-form-urlencoded",
	"User-Agent" : "User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Referer" : "http://poe.trade/",
	"Accept-Encoding" : "gzip, deflate",
	"Accept-Language" : "en-US,en;q=0.9",
	"Cookie" : "_ga=GA1.2.206788054.1525455159; __cfduid=dc212bce0ec374351dd9bcebeae36c5501525493980; league=Bestiary; _gid=GA1.2.2088975945.1526632014"
}
#league=Bestiary^&type=^&base=^&name=kaom^%^27s+heart^&dmg_min=^&dmg_max=^&aps_min=^&aps_max=^&crit_min=^&crit_max=^&dps_min=^&dps_max=^&edps_min=^&edps_max=^&pdps_min=^&pdps_max=^&armour_min=^&armour_max=^&evasion_min=^&evasion_max=^&shield_min=^&shield_max=^&block_min=^&block_max=^&sockets_min=^&sockets_max=^&link_min=^&link_max=^&sockets_r=^&sockets_g=^&sockets_b=^&sockets_w=^&linked_r=^&linked_g=^&linked_b=^&linked_w=^&rlevel_min=^&rlevel_max=^&rstr_min=^&rstr_max=^&rdex_min=^&rdex_max=^&rint_min=^&rint_max=^&mod_name=^&mod_min=^&mod_max=^&mod_weight=^&group_type=And^&group_min=^&group_max=^&group_count=1^&q_min=^&q_max=^&level_min=^&level_max=^&ilvl_min=^&ilvl_max=^&rarity=^&seller=^&thread=^&identified=^&corrupted=^&progress_min=^&progress_max=^&sockets_a_min=^&sockets_a_max=^&shaper=^&elder=^&map_series=^&crafted=^&enchanted=^&online=x^&altart=^&capquality=x^&buyout_min=^&buyout_max=^&buyout_currency=^&has_buyout=^&exact_currency=
session = HTMLSession()

searches = [
	{
		"league":"Bestiary",
		"name":"Fenumus' Shroud",
		"online":"x"
	}
]

for armor in list(armor_values.keys()):
	newsearch = {}
	newsearch['league'] = 'Bestiary'
	newsearch['name'] = armor
	newsearch['online'] = 'x'
	searches.append(newsearch)


#for search in searches:
#	response = requests.post('http://poe.trade/search', headers=headers, data=search)
#	webbrowser.open_new_tab(response.url)
for search in searches:
	response = session.post('http://poe.trade/search', headers=headers, data=search)
	#webbrowser.open_new_tab(response.url)
	lines = response.html.find(".item")
	prices = []
	#print(search['name'])
	for line in lines:
		attributes = line.attrs
		data_buyout = attributes['data-buyout']
		if data_buyout:
			amount = re.search("(\w+) (\w{3,5})", data_buyout).group(1)
			match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)
			#print(amount + " " + match)
			for key, value in parsed_rates_data.items():
				check = re.search(match, key, re.IGNORECASE)
				if check:
					amount_in_chaos = int(amount)*float(value)
					prices.append(amount_in_chaos)
	print(search['name'] + " | Average price in poe.trade: " + str(sum(prices)/len(prices)) + " #offers: " + str(len(prices)) + " | Price from poe.ninja: " + str(armor_values[search['name']]))

	#webbrowser.open_new_tab(session.next
#print(response.text)
#htmlfile = open('pop.html', 'w', encoding='utf-8')
#htmlfile.write(response.text)
#htmlfile.close()

#webbrowser.open_new_tab(response.url)
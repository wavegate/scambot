import requests
from requests_html import HTMLSession
import re
import json
import webbrowser
import searches
import winsound

rates_data = requests.get("http://poe.ninja/api/Data/GetCurrencyOverview?league=Bestiary").json()
parsed_rates_data = {}

urls = [
	"http://poe.ninja/api/Data/GetUniqueFlaskOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetDivinationCardsOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetProphecyOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetUniqueArmourOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetUniqueWeaponOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetUniqueMapOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetUniqueJewelOverview?league=Bestiary",
	"http://poe.ninja/api/Data/GetEssenceOverview?league=Bestiary",
]

CURRENCY_PRICES_URL : "http://poe.ninja/api/Data/GetCurrencyOverview?league=Bestiary"

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

unique_data = {}

for url in urls:
	url_data = requests.get(url).json()
	if url_data:
		for item_data in url_data['lines']:
			unique_data[item_data['name']] = item_data['chaosValue']

headers = {
	"Connection" : "keep-alive",
	"Cache-Control" : "max-age=0",
	"Origin" : "http://poe.trade",
	"Upgrade-Insecure-Requests" : "1",
	"Content-Type" : "application/x-ww	w-form-urlencoded",
	"User-Agent" : "User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
	"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Referer" : "http://poe.trade/",
	"Accept-Encoding" : "gzip, deflate",
	"Accept-Language" : "en-US,en;q=0.9",
	"Cookie" : "_ga=GA1.2.206788054.1525455159; __cfduid=dc212bce0ec374351dd9bcebeae36c5501525493980; league=Bestiary; _gid=GA1.2.2088975945.1526632014"
}

searches = []

for unique in unique_data:
	search = {}
	search['name'] = unique
	search['league'] = 'Bestiary'
	search['online'] = 'x'
	search['corrupted'] = '0'
	searches.append(search)

session = HTMLSession()

good_trades = []

def cheapest():
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		line = response.html.find(".item", first=True)
		if line:
			attributes = line.attrs
			data_buyout = attributes['data-buyout']
			if data_buyout:
				amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", data_buyout).group(1)
				match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)
				item_value = float(unique_data[search['name']])
				if match != "chaos":
					for key, value in parsed_rates_data.items():
						check = re.search(match, key, re.IGNORECASE)
						if check:
							amount = float(amount)*float(value)
				amount = float(amount)
				difference = item_value - amount
				toprint = search['name'] + ": " + str(item_value) + " - " + str(amount) + " = " + str(difference)
				print(toprint)
				if difference > 10:
					good_trades.append(search['name'])
					winsound.Beep(1000, 500)
					with open("pop.txt", "a") as myfile:
						myfile.write(search['name'] + "\n")
					print("!!!!!!!!!!!!!!!!!!!!!!!!!")

cheapest()

def average():
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		#webbrowser.open_new_tab(response.url)
		lines = response.html.find(".item")
		print("searching... " + search['name'])
		prices = []
		for line in lines:
			attributes = line.attrs
			data_buyout = attributes['data-buyout']
			if data_buyout:
				amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", data_buyout).group(1)
				match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)	
				#print(amount + " " + match)
				for key, value in parsed_rates_data.items():
					check = re.search(match, key, re.IGNORECASE)
					if check:
						amount_in_chaos = float(amount)*float(value)
						item_value = int(unique_data[search['name']])
						#print(str(amount_in_chaos) + " " + str(item_value))
						if amount_in_chaos < (item_value - 1):
							good_trades.append(attributes)
							prices.append(amount_in_chaos)
		#one = dict(search)['name']
		#if len(prices) > 0:
		#	print(one + " | Average price in poe.trade: " + str(sum(prices)/len(prices)) + " #offers: " + str(len(prices)))

#for item in good_trades:
#	print(item)
import requests
from requests_html import HTMLSession
import re
import json
import webbrowser
import searches
import winsound
import pyperclip
import pyautogui
import time
import random
import autogui

#Post limit, maximum pastes per 24h reached

session = HTMLSession()

urls = [
	"http://poe.ninja/api/Data/GetUniqueFlaskOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetDivinationCardsOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetProphecyOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetUniqueArmourOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetUniqueWeaponOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetUniqueMapOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetUniqueJewelOverview?league=Incursion",
	"http://poe.ninja/api/Data/GetEssenceOverview?league=Incursion",
]

CURRENCY_PRICES_URL : "http://poe.ninja/api/Data/GetCurrencyOverview?league=Incursion"

CURRENCY_FULL = ['Orb of Alteration', 'Orb of Fusing',
                 'Orb of Alchemy', 'Chaos Orb',
                 'Gemcutter\'s Prism', 'Exalted Orb',
                 'Chromatic Orb', 'Jeweller\'s Orb',
                 'Orb of Chance', 'Cartographer\'s Chisel',
                 'Orb of Scouring', 'Blessed Orb',
                 'Orb of Regret', 'Regal Orb', 'Divine Orb',
                 'Vaal Orb']
parsed_rates_data = {}
good_trades = []

def findRates():
	rates_data = requests.get("http://poe.ninja/api/Data/GetCurrencyOverview?league=Incursion").json()

	if rates_data:
	    for currency_data in rates_data['lines']:
	        if currency_data['currencyTypeName'] in CURRENCY_FULL:
	            parsed_rates_data[currency_data['currencyTypeName']] = currency_data['chaosEquivalent']

def parseNinja(urls):
	unique_data = {}
	for url in urls:
		url_data = requests.get(url).json()
		if url_data:
			for item_data in url_data['lines']:
				unique_data[item_data['name']] = item_data['chaosValue']
	return unique_data

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
	"Cookie" : "_ga=GA1.2.206788054.1525455159; __cfduid=dc212bce0ec374351dd9bcebeae36c5501525493980; league=Incursion; _gid=GA1.2.2088975945.1526632014"
}

def buildSearches(unique_data):
	searches = []
	for unique in unique_data:
		search = {}
		search['name'] = unique
		search['league'] = 'Incursion'
		search['online'] = 'x'
		search['corrupted'] = '0'
		searches.append(search)
	return searches

def tradepage():
	pyautogui.PAUSE = 0.2
	unique_data = []
	unique_data.append(input("What? "))
	maxCost = 12
	searches = buildSearches(unique_data)
	search = searches[0]
	response = session.post('http://poe.trade/search', headers=headers, data=search)
	lines = response.html.find(".item")
	count = 0
	sellers = []
	autogui.switchtopoe()
	if lines:
		for line in lines:
			if count >= 20:
				break
			attributes = line.attrs
			seller = attributes['data-ign']
			if seller not in sellers:
				name = attributes['data-name']
				league = attributes['data-league']
				buyout = attributes['data-buyout']
				if chaosValue(buyout) <= maxCost:
					tab = attributes['data-tab']
					x = attributes['data-x']
					y = attributes['data-y']
					string = '@{} Hi, I would like to buy your {} listed for {} in {} (stash tab "{}"; position: left {}, top {})'.format(seller, name, buyout, league, tab, x, y)
					pyperclip.copy(string)
					pyautogui.press('enter')
					time.sleep(random.uniform(0.3, 0.6))
					pyautogui.hotkey('ctrl', 'a')
					time.sleep(random.uniform(0.3, 0.6))
					pyautogui.hotkey('ctrl', 'v')
					time.sleep(random.uniform(0.3, 0.6))
					pyautogui.press('enter')
					sellers.append(seller)
					count = count + 1

def chaosValue(buyout):
	amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", buyout).group(1)
	match = re.search("(\w+) (\w{3,5})", buyout).group(2)
	if match != "chaos":
		for key, value in parsed_rates_data.items():
			check = re.search(match, key, re.IGNORECASE)
			if check:
				amount = float(amount)*float(value)
	amount = float(amount)
	return amount



def cheapest(searches, unique_data):
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		line = response.html.find(".item", first=True)
		#webbrowser.open_new_tab(response.url)
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
				toprint = search['name'] + ": " + str(item_value) + " - " + str(amount) + " = " + str(difference) + " " + str(difference/item_value)
				print(toprint)
				if difference >= 10:
					good_trades.append(search['name'])
					winsound.Beep(1000, 500)
					with open("pop.txt", "a") as myfile:
						myfile.write(toprint + "\n")
						if difference/item_value > 0.5:
							myfile.write("xxxxxxxxxx\n")
							webbrowser.open_new_tab(response.url)
					print("!!!!!!!!!!!!!!!!!!!!!!!!!")

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

card_data = {}

def divinationCards():
	url_data = requests.get("http://poe.ninja/api/Data/GetDivinationCardsOverview?league=Incursion").json()
	if url_data:
		for item_data in url_data['lines']:
			card_data[item_data['name']] = [item_data['chaosValue'], item_data['explicitModifiers'][0]['text']]

def searchList(searchList):
	searches = []
	for unique in unique_data:
		if unique in searchList:
			search = {}
			search['name'] = unique
			search['league'] = 'Incursion'
			search['online'] = 'x'
			search['corrupted'] = '0'
			searches.append(search)
	cheapest(searches)

def theTaming():
	tamingItems= ["The Spark and the Flame", "Berek's Respite", "Berek's Pass", "Berek's Grip", "The Taming"]
	searchList(tamingItems)

def openMaps(tier):
	urls = ['http://poe.ninja/api/Data/GetMapOverview?league=Incursion']
	unique_data = {}
	for url in urls:
		url_data = requests.get(url).json()
		if url_data:
			for item_data in url_data['lines']:
				if item_data['mapTier'] == tier:
					unique_data[item_data['name']] = [item_data['chaosValue'], item_data['mapTier']]
	searches = []
	for unique in unique_data:
		search = {}
		search['name'] = unique
		search['league'] = 'Incursion'
		search['online'] = 'x'
		search['corrupted'] = '0'
		search['level_min'] = unique_data[unique][1]
		search['level_max'] = unique_data[unique][1]
		searches.append(search)
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		line = response.html.find(".item", first=True)
		webbrowser.open_new_tab(response.url)
		if line:
			attributes = line.attrs
			data_buyout = attributes['data-buyout']
			if data_buyout:
				amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", data_buyout).group(1)
				match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)
				item_value = float(unique_data[search['name']][0])
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
					#webbrowser.open_new_tab(response.url)
					winsound.Beep(1000, 500)
					with open("pop.txt", "a") as myfile:
						myfile.write(search['name'] + "\n")
					print("!!!!!!!!!!!!!!!!!!!!!!!!!")

def maps():
	urls = ['http://poe.ninja/api/Data/GetMapOverview?league=Incursion']
	unique_data = {}
	for url in urls:
		url_data = requests.get(url).json()
		if url_data:
			for item_data in url_data['lines']:
				unique_data[item_data['name']] = [item_data['chaosValue'], item_data['mapTier']]
	searches = []
	for unique in unique_data:
		search = {}
		search['name'] = unique
		search['league'] = 'Incursion'
		search['online'] = 'x'
		search['corrupted'] = '0'
		search['level_min'] = unique_data[unique][1]
		search['level_max'] = unique_data[unique][1]
		searches.append(search)
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		line = response.html.find(".item", first=True)
		#webbrowser.open_new_tab(response.url)
		if line:
			attributes = line.attrs
			data_buyout = attributes['data-buyout']
			if data_buyout:
				amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", data_buyout).group(1)
				match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)
				item_value = float(unique_data[search['name']][0])
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
					#webbrowser.open_new_tab(response.url)
					winsound.Beep(1000, 500)
					with open("pop.txt", "a") as myfile:
						myfile.write(search['name'] + "\n")
					print("!!!!!!!!!!!!!!!!!!!!!!!!!")

def prophecies():
	urls = ['http://poe.ninja/api/Data/GetProphecyOverview?league=Standard']
	unique_data = {}
	for url in urls:
		url_data = requests.get(url).json()
		if url_data:
			for item_data in url_data['lines']:
				unique_data[item_data['name']] = [item_data['chaosValue']]
	searches = []
	for unique in unique_data:
		search = {}
		search['name'] = unique
		search['league'] = 'Standard'
		search['online'] = 'x'
		search['corrupted'] = '0'
		searches.append(search)
	for search in searches:
		response = session.post('http://poe.trade/search', headers=headers, data=search)
		line = response.html.find(".item", first=True)
		#webbrowser.open_new_tab(response.url)
		if line:
			attributes = line.attrs
			data_buyout = attributes['data-buyout']
			if data_buyout:
				amount = re.search("(\d{0,4}\.?\d{0,2}) (\w{3,5})", data_buyout).group(1)
				match = re.search("(\w+) (\w{3,5})", data_buyout).group(2)
				item_value = float(unique_data[search['name']][0])
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
					#webbrowser.open_new_tab(response.url)
					winsound.Beep(1000, 500)
					with open("pop.txt", "a") as myfile:
						myfile.write(search['name'] + "\n")
					print("!!!!!!!!!!!!!!!!!!!!!!!!!")

def allUniques():
	unique_data = parseNinja(urls)
	searches = buildSearches(unique_data)
	cheapest(searches, unique_data)

findRates()
tradepage()
#openMaps(6)
#allUniques()

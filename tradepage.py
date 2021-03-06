import requests
import webbrowser
from requests_html import HTMLSession

session = HTMLSession()

search = [('league', 'Bestiary'),
	  ('type', ''),
	  ('base', ''),
	  ('name', 'Kaom\'s Heart'),
	  ('dmg_min', ''),
	  ('dmg_max', ''),
	  ('aps_min', ''),
	  ('aps_max', ''),
	  ('crit_min', ''),
	  ('crit_max', ''),
	  ('dps_min', ''),
	  ('dps_max', ''),
	  ('edps_min', ''),
	  ('edps_max', ''),
	  ('pdps_min', ''),
	  ('pdps_max', ''),
	  ('armour_min', ''),
	  ('armour_max', ''),
	  ('evasion_min', ''),
	  ('evasion_max', ''),
	  ('shield_min', ''),
	  ('shield_max', ''),
	  ('block_min', ''),
	  ('block_max', ''),
	  ('sockets_min', ''),
	  ('sockets_max', ''),
	  ('link_min', ''),
	  ('link_max', ''),
	  ('sockets_r', ''),
	  ('sockets_g', ''),
	  ('sockets_b', ''),
	  ('sockets_w', ''),
	  ('linked_r', ''),
	  ('linked_g', ''),
	  ('linked_b', ''),
	  ('linked_w', ''),
	  ('rlevel_min', ''),
	  ('rlevel_max', ''),
	  ('rstr_min', ''),
	  ('rstr_max', ''),
	  ('rdex_min', ''),
	  ('rdex_max', ''),
	  ('rint_min', ''),
	  ('rint_max', ''),
	  ('mod_name', '#% increased Fire Damage'),
	  ('mod_min', '35'),
	  ('mod_max', ''),
	  ('mod_weight', ''),
	  ('group_type', 'And'),
	  ('group_min', ''),
	  ('group_max', ''),
	  ('group_count', '1'),
	  ('q_min', ''),
	  ('q_max', ''),
	  ('level_min', ''),
	  ('level_max', ''),
	  ('ilvl_min', ''),
	  ('ilvl_max', ''),
	  ('rarity', ''),
	  ('seller', ''),
	  ('thread', ''),
	  ('identified', ''),
	  ('corrupted', ''),
	  ('progress_min', ''),
	  ('progress_max', ''),
	  ('sockets_a_min', ''),
	  ('sockets_a_max', ''),
	  ('shaper', ''),
	  ('elder', ''),
	  ('map_series', ''),
	  ('crafted', ''),
	  ('enchanted', ''),
	  ('online', 'x'),
	  ('altart', ''),
	  ('capquality', 'x'),
	  ('buyout_min', ''),
	  ('buyout_max', ''),
	  ('buyout_currency', ''),
	  ('has_buyout', ''),
	  ('exact_currency', ''),]

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

def findRates():
	rates_data = session.get("http://poe.ninja/api/Data/GetCurrencyOverview?league=Incursion").json()

	if rates_data:
	    for currency_data in rates_data['lines']:
	        if currency_data['currencyTypeName'] in CURRENCY_FULL:
	            parsed_rates_data[currency_data['currencyTypeName']] = currency_data['chaosEquivalent']

response = session.post('http://poe.trade/search', headers=headers, data=search)
line = response.html.find(".item")
#webbrowser.open_new_tab(response.url)
print(line[0])
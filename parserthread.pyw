import threading

import requests

import constants

import re

import csv

class ParserThread(threading.Thread):
    """Thread that parses each chunk of stash API data"""

    def __init__(self, spawner, parse_id, params_list, exchange_rates):
        """Initializes the thread with a reference to the creator thread and specified search parameters."""
        threading.Thread.__init__(self)
        self.dead = False
        self.spawner = spawner
        self.parse_id = parse_id
        self.params_list = params_list
        self.exchange_rates = exchange_rates
        self.start()
        self.filename = "results.csv"

    def run(self):
        """Main actions of thread.
        First reads the API into an dictionary before parsing that dictionary for the desired items.
        """
        self.get_stashes()
        self.parse_stashes()

    def kill(self):
        """Sets the flag to stop processing and terminate the thread."""
        self.dead = True

    def get_stashes(self):
        """Reads the JSON data from the stash API into a dictionary.
        Also returns the id of the next chunk of data to the main thread via queue.
        """
        stash_data = requests.get(constants.STASH_API + self.parse_id).json()
        self.spawner.queue_parse_ids.put(stash_data['next_change_id'])
        self.stashes = stash_data['stashes']

    def parse_stashes(self):
        """Parses the stash data for items matching input specifications.
        Returns matching items to the main thread via queue.
        """
        for stash in self.stashes:
            for item in stash['items']:
                if self.dead:
                    return
                for params in self.params_list:
                    checked_item = self.check_item(item, stash, params)
                    if checked_item:
                        self.spawner.finds.append(item)
                        self.spawner.queue_results.put({'name':stash['lastCharacterName'], 'item':checked_item[0],
                                                        'price':checked_item[1], 'league':item['league'],
                                                        'stash':stash['stash'], 'x':item['x'], 'y':item['y']})

    def check_item(self, item, stash, params):
        """Checks whether the item matches specifications."""

        #if item['frameType'] and item['frameType'] == 5:
        #    return None

        #if 'league' in params:
        #    if not item['league'] == params['league']:
        #        return None

        categoryValues = list(item['category'].values())[0]
        if 'category' in params:
            if categoryValues:
                if params['category'] != categoryValues[0]:
                    return None
            else:
                if params['category'] not in item['category']:
                    return None

        #if params['base'] != 'any':
        #    if params['base'] not in item['typeLine']:
        #        return None

        #if params['corrupted'] == 'True' and item['corrupted'] == 'False':
        #    return None

        #if not params['crafted'] and 'craftedMods' in item:
        #    return None

        #if not params['frame type'] == item['frameType']:
        #    return None

        #p = re.compile("\d+")
        #x = p.search(item['explicitMods'][0])
        #v = int(x.group(0))
        #print(v)

        if 'name' in params:
            namematch = re.search(params['name'], item['name'], re.IGNORECASE)
            typelinematch = re.search(params['name'], item['typeLine'], re.IGNORECASE)
            if namematch is None and typelinematch is None:
                return None

        if 'explicits' in params:
            for search_explicit in params['explicits']:
                search_value = re.search("\d+", search_explicit).group(0)
                found = False
                if'explicitMods' in item:
                    for item_explicit in item['explicitMods']:
                        item_mod = re.search("\d+(.*)", item_explicit)
                        if item_mod:
                            if item_mod.group(1) in search_explicit:
                                found = True
                                if item_mod.group(0) < search_value:
                                    return None
                if not found:
                    return None
                #if value > :
                #    return None
                #print(item)

        #print(item['sockets'])
        #if len(item['sockets']) < params['sockets']:
        #    return None

        #if not self.check_links(item['sockets'], params['links']):
        #    return None

        full_name = constants.LOCALIZATION.sub('', ' '.join(filter(None, [item['name'], item['typeLine']])))
        full_text = ' '.join([full_name] + (item['implicitMods'] if 'implicitMods' in item else []) + (item['explicitMods'] if 'explicitMods' in item else []))
        #if not params['regex'].search(full_text):
        #    return None

        price_regex_match = constants.PRICE_REGEX.match(stash['stash'])
        try:
            price_regex_match = constants.PRICE_REGEX.match(item['note'])
        except KeyError:
            pass
        
        if not price_regex_match:
            return None

        # In essence, uses the league's exchange rates to get item's value in chaos
        price = float(price_regex_match.group(2)) * self.exchange_rates[params['league']].get(constants.CURRENCY_FULL[constants.CURRENCY_ABBREVIATED.index(price_regex_match.group(3))], 1.0)

        #if price > params['maxprice'] or price < params['minprice']:
        #    return None

        with open(self.filename, 'a+') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([item['name'], item['typeLine'], stash['accountName'], item['id'], item['explicitMods']])

        #self.spawner.log.append(item)
        return full_text, price_regex_match

    def check_links(self, item_sockets, links):
        """Checks whether the item has the desired number of links."""
        groups = [0] * 6
        for socket in item_sockets:
            groups[socket['group']] += 1
        for i in groups:
            if i >= links:
                return True
        return False
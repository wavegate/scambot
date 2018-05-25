import requests
from requests_html import HTMLSession

cookies = {
    'stored_data': '1',
    '__utmc': '183580967',
    'visited_overview': '1',
    'POESESSID': 'e1d4d009516dc0c3c90ceedd8511b38c',
    'session_start': '1526526775',
    '__utma': '183580967.2124089286.1525491184.1526969910.1526981144.14',
    '__utmz': '183580967.1526981144.14.9.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    '__utmt': '1',
    '__utmb': '183580967.4.10.1526981144',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://www.pathofexile.com/forum/view-forum/24',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

session = HTMLSession()
response = session.get('https://www.pathofexile.com/forum/view-thread/1764075')
title = response.html.find(".layoutBoxTitle", first=True).text
items = response.html.find(".itemContentLayout")
print(str(items))


"""
filename = "forumanalyzer.txt"
file = open(filename, "w")
file.write(response.text)
"""
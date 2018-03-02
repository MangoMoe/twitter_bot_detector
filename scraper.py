import requests
from bs4 import BeautifulSoup

r = requests.get('https://botwiki.org/tag/twitterbot/')
soup = BeautifulSoup(r.content, "html.parser")
elements = soup.select("div.row.search-item")
with open('bots.txt', 'w') as bots:
    for el in elements:
        bot = el.select('h4 a')
        if bot:
            bots.write(bot[0].text.replace('@', '') + '\n')

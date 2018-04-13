"""
"""

import re
import sys
import json
import collections
import bs4
import requests

DEFAULT_BASE_URL = 'https://eresearch.fidelity.com/eresearch/evaluate/fundamentals/keyStatistics.jhtml?stockspage=keyStatistics&symbols='

def getUrl(symbol):
    """
    """
    return DEFAULT_BASE_URL + symbol

def getSoup(url):
    """
    """
    res = requests.get(url)
    return bs4.BeautifulSoup(res.content, 'html.parser')

def getName(soup):
    """
    """
    h2 = soup.find('h2', {'id': 'companyName'})
    return h2.text

def getRows(soup):
    """
    """
    rows = []
    tables = soup.find_all('table', {'class': 'datatable-component'})
    for table in tables:
        tri = table.find_all('tr')
        rows = rows + [tr for tr in tri if len(tr.find_all('td')) is 5]
    return rows

def getProps(rows):
    """
    """
    props = {}
    for row in rows:
        tdi = row.find_all('td')
        key = tdi[0].text.strip()
        value = tdi[1].text.strip()
        props[key] = value
    return props

def capitalize(name):
    """Lower-cases each letter in each word, except the first (capitalized).
    """
    words = name.split()
    for ndx in range(len(words)):
        word = words[ndx]
        words[ndx] = word[0].upper() + word[1:].lower()
    return ' '.join(words)

def main(symbol):
    """
    """
    url = getUrl(symbol)
    soup = getSoup(url)
    rows = getRows(soup)
    name = getName(soup)
    company = collections.OrderedDict({
        'name': capitalize(name),
        'symbol': symbol
    })
    company.update(getProps(rows))
    return company

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Command-line invocation requires a ticker symbol')
    COMPANY = main(sys.argv[1])
    print(json.dumps(COMPANY, indent=4))    

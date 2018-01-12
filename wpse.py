"""Defines a scraper for pulling stock exchange data from a Wikipedia page
"""

import io
import csv
import warnings
import bs4
import requests

def getUrl():
    """
    """
    return 'https://en.wikipedia.org/wiki/List_of_stock_exchanges'

def getWikiTable(url):
    """
    """
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html5lib')
    wikitables = soup.find_all('table', {'class': 'wikitable'})
    if len(wikitables) is not 1:
        raise Exception('Unable to resolve singular wikitable')
    return wikitables[0]

def convertToFieldHeader(text):
    """
    """
    fieldHeader = '_'
    safe = text.encode('ascii', errors='ignore')
    try:
        title = safe.splitlines()[0]
        parts = title.decode('ascii').split(' ')
        for ndx, part in enumerate(parts):
            if ndx == 0:
                parts[ndx] = part.lower()
            else:
                parts[ndx] = part[0].upper() + part[1:].lower()
        fieldHeader = ''.join(parts)
    except Exception as e:
        warnings.warn('Failed to parse valid field header from "%s"; defaulting to %s' % (safe, fieldHeader))
    return fieldHeader

def parseTable(table):
    """Converts a wikitable BS4 element to a header and list of row tuples
    """
    thi = table.find_all('th')
    header = [convertToFieldHeader(th.text) for th in thi]
    tri = table.find_all('tr')
    entries = []
    for tr in tri[1:]:
        tdi = tr.find_all('td')
        entry = [td.text.encode('ascii', errors='ignore').decode('ascii') for td in tdi]
        entries.append(tuple(entry))
    return header, entries
    
def convertNumberCols(entries):
    """If all entries in a given column can be converted to numeric values (integers or floats),
       they are.
    """
    entries = [list(entry) for entry in entries]
    nCols = len(entries[0])
    for i in range(nCols):
        try:
            values = [float(entry[i].replace(',', '')) for entry in entries]
            for j, entry in enumerate(entries):
                entry[i] = values[j]
        except Exception as e:
            continue
    entries = [tuple(entry) for entry in entries]
    return entries

def tableToDicts(header, entries):
    """Converts a tuple of header names, and a list of entry tuples, to a list of dictionaries
    """
    dicts = []
    for entry in entries:
        dicts.append(dict(zip(header, entry)))
    return dicts

def writeToCsv(dicts):
    """
    """
    sio = io.StringIO()
    dw = csv.DictWriter(sio, fieldnames=dicts[0].keys(), lineterminator='\n')
    dw.writeheader()
    for obj in dicts:
        dw.writerow(obj)
    sio.seek(0)
    return sio.read()

def main():
    """
    """
    url = getUrl()
    table = getWikiTable(url)
    header, entries = parseTable(table)
    # remove Israel by hand, as it currently has no numeric entries
    economy_ndx = header.index('economy')
    economies = [entry[economy_ndx] for entry in entries]
    israel_ndx = economies.index('Israel')
    entries.pop(israel_ndx)
    # continue as normal
    entries = convertNumberCols(entries)
    return tableToDicts(header, entries)
    

if __name__ == "__main__":
    result = main()
    print(writeToCsv(result))


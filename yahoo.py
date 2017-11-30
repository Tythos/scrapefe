"""
"""

import io
import re
import bs4
import csv
import sys
import requests
import datetime
import warnings

def search(term):
    """
    """
    return "https://finance.yahoo.com/quote/%s/history?p=%s" % (term, term)
    
def fetch(url):
    """
    """
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, 'html5lib')
    table = soup.find('table')
    tri = table.find_all('tr')
    return tri
    
def parse(rows):
    """
    """
    thi = rows[0].find_all('th')
    headers = tuple([re.sub('[^\w]', '', th.text).lower() for th in thi])
    date_ndx = headers.index('date')
    entries = []
    for i, row in enumerate(rows[1:]):
        try:
            tdi = row.find_all('td')
            values = [td.text for td in tdi]
            entry = []
            for j, value in enumerate(values):
                if j == date_ndx:
                    dt = datetime.datetime.strptime(value, '%b %d, %Y')
                    entry.append(dt.date())
                else:
                    entry.append(float(value.replace(',', '')))
            entries.append(tuple(entry))
        except Exception as e:
            warnings.warn('Unable to parse row #%u' % i)
    return headers, entries    
    
def convertToObjs(headers, entries):
    """
    """
    return [dict(zip(headers, entry)) for entry in entries]

def toCsv(objs):
    """
    """
    sio = io.StringIO()
    dw = csv.DictWriter(sio, fieldnames=objs[0].keys(), lineterminator='\n')
    dw.writeheader()
    for obj in objs:
        dw.writerow(obj)
    sio.seek(0)
    return sio.read()
    
def main(term):
    """
    """
    url = search(term)
    rows = fetch(url)
    headers, entries = parse(rows)
    return convertToObjs(headers, entries)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Command-line invocation requires a search term (ticker symbol)")
    result = main(sys.argv[1])
    print(toCsv(result))

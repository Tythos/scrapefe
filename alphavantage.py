"""
"""

import io
import os
import csv
import time
import datetime
import numpy
import requests

def getApiKey():
    """
    """
    packPath, _ = os.path.split(__file__)
    keyPath = packPath + os.path.sep + 'keys'
    with open(keyPath + os.path.sep + 'alphavantage.txt') as f:
        return f.read().strip()

def getHistory(symbol):
    """Does a full pull of historical data from Alpha Vantage API.
    """
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': getApiKey(),
        'datatype': 'csv',
        'outputsize': 'full'
    }
    res = requests.get(url, params=params)
    content = res.content.decode('ascii')
    rdr = csv.reader(io.StringIO(content))
    table = [row for row in rdr]
    header = tuple(table[0])
    timestamp_ndx = header.index('timestamp')
    entries = []
    for row in table[1:]:
        entry = []
        for jj, col in enumerate(row):
            if jj is timestamp_ndx:
                dt = datetime.datetime.strptime(col, '%Y-%m-%d')
                value = time.mktime(dt.timetuple())
            else:
                value = float(col)
            entry.append(value)
        entries.append(entry)
    return header, numpy.array(entries)

def main():
    """
    """
    header, table = getHistory('SQ')
    print(header)
    print(table[:10,:])

if __name__ == "__main__":
    main()

"""
"""

import io
import os
import csv
import time
import datetime
import numpy
import requests
from scrapefe import keys

DEFAULT_BASE_URL = 'https://www.alphavantage.co/query'

def getRecent(symbol):
    """Does a recent-only pull of historical data from the Alpha Vantage API.
    """
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': keys.get('alphavantage.tok'),
        'datatype': 'csv',
        'outputsize': 'compact'
    }
    res = requests.get(DEFAULT_BASE_URL, params=params)
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

def getHistory(symbol):
    """Does a full pull of historical data from Alpha Vantage API.
    """
    params = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'symbol': symbol,
        'apikey': keys.get('alphavantage.tok'),
        'datatype': 'csv',
        'outputsize': 'full'
    }
    res = requests.get(DEFAULT_BASE_URL, params=params)
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

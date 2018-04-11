"""
"""

import os
import re
import csv
import numpy
from scrapefe import alphavantage

class Security(object):
    """
    """
    
    def __init__(self, csvPath):
        """Defines a security as a one-to-one correlation with a CSV file
           containing a historical data table.
        """
        self.absPath, fileName = os.path.split(csvPath)
        symbol, _ = os.path.splitext(fileName)
        self.symbol = symbol.lower()
        with open(csvPath, 'r') as f:
            rdr = csv.reader(f)
            rows = [row for row in rdr]
        self.header = rows[0]
        for ndx in range(1,len(rows)):
            rows[ndx] = [float(v) for v in rows[ndx]]
        self.table = numpy.array(rows[1:])

    def getSeries(self, name):
        """
        """
        col_ndx = self.header.index(name)
        return self.table[:,col_ndx]

    def update(self):
        """Splices new entries from alphavantage to update historical data
           table.
        """
        header, table = alphavantage.getRecent(self.symbol)
        if len(header) is not len(self.header) or any([header[i] != self.header[i] for i in range(len(header))]):
            raise Exception('Headers mismatch; pivot required before update')
        tsNew_ndx = header.index('timestamp')
        mostRecent_ts = max(self.getSeries('timestamp'))
        toSplice_flags = table[:,tsNew_ndx] > mostRecent_ts
        if not any(toSplice_flags):
            header, table = alphavantage.getHistory(self.symbol)
            tsNew_ndx = header.index('timestamp')
            toSplice_flags = table[:,tsNew_ndx] > mostRecent_ts
        newRows = table[toSplice_flags,:]
        self.table = numpy.append(newRows, self.table, axis=0)

    def save(self):
        """
        """
        csvPath = '%s%s%s.csv' % (self.absPath, os.path.sep, self.symbol)
        with open(csvPath, 'w') as f:
            wtr = csv.writer(f, lineterminator='\n')
            wtr.writerows([self.header])
            wtr.writerows(self.table)

class Portfolio(object):
    """
    """

    def __init__(self, listPath):
        """Defines a portfolio as a one-to-one correlation with a symbol
           listing, co-located with a set of .CSV files for historical data of
           each symbol security.
        """
        self.path, fileName = os.path.split(listPath)
        self.name, _ = os.path.splitext(fileName)
        with open(listPath, 'r') as f:
            txt = f.read()
        entries = re.split('\s+', txt)
        self.symbols = [entry.lower() for entry in entries]

    def getSecurity(self, symbol):
        """
        """
        if symbol not in self.symbols:
            raise Exception('Symbol "%s" not in portfolio' % symbol)
        csvPath = '%s%s%s.csv' % (self.path, os.path.sep, symbol)
        if not os.path.isfile(csvPath):
            header, table = alphavantage.getHistory(symbol)
            with open(csvPath, 'w') as f:
                wtr = csv.writer(f, lineterminator='\n')
                wtr.writerows([header])
                wtr.writerows(table)
        return Security(csvPath)

    def addSecurity(self, symbol):
        """Adds a new symbol and returns the new Security object. (A pull will
           implicitly be performed by *getSecurity()* to create a new CSV.)
        """
        if symbol in self.symbols:
            raise Exception('Symbol "%s" is already in portfolio' % symbol)
        self.symbols.append(symbol)
        return self.getSecurity(symbol)

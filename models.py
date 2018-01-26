"""Common models for capturing exchange, index, security, and historical data
"""

import numpy
from scrapefe import alphavantage as av

class HistDat(object):
    """
    """

    def __init__(self, symbol):
        """
        """
        self.symbol = symbol
        self.header = tuple()
        self.table = numpy.array([])

    def initialize(self):
        """Generate an initial dataset from full pull
        """
        self.header, self.table = av.getHistory(self.symbol)

    def update(self):
        """Update existing dataset with recent entries
        """
        pass

    def toXLSX(self, xlsxPath):
        """Save existing datset to xlsx worksheet. Sheet name is security
           symbol.
        """
        pass

    @classmethod
    def fromXLSX(self, xlsxPath, sheetName):
        """Load existing dataset from xlsx worksheet
        """
        pass

def test():
    """
    """
    xlsxPath = __file__.replace('.py', '.xlsx')
    sq = HistDat('SQ')
    sq.initialize()
    sq.toXLSX(xlsxPath)
    coke = HistDat.fromXLSX(xlsxPath, 'COKE')
    coke.update()

if __name__ == "__main__":
    test()

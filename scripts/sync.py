"""Adds a specific security to the package *data/* folder, if it does not
   exist. If it does, updates entries with the latest data.
"""

import os
import sys
from scrapefe import models, data

def main(symbol):
    """
    """
    symbol = symbol.lower()
    xlsxPath = '%s%s%s.xlsx' % (data.getAbsPath(), os.path.sep, symbol)
    if os.path.isfile(xlsxPath):
        print('Loading, updating existing historical dataset')
        hd = models.HistDat.fromXLSX(xlsxPath)
        hd.update()
    else:
        print('Initializing new historical dataset')
        hd = models.HistDat(symbol)
        hd.initialize()
    print('Writing historical data to file')
    hd.toXLSX(xlsxPath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Command-line invocation requires a security symbol')
    main(sys.argv[1])

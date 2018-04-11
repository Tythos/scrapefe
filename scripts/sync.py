"""Adds a specific security to the package *data/* folder, if it does not
   exist. If it does, updates entries with the latest data.
"""

import os
import csv
import sys
from scrapefe import data, models, alphavantage

def main(symbol):
    """By default, creates/updates CSV in package data folder
    """
    symbol = symbol.lower()
    csvPath = '%s%s%s.csv' % (data.getAbsPath(), os.path.sep, symbol)
    if os.path.isfile(csvPath):
        print('Loading, updating existing historical dataset')
        sec = models.Security(csvPath)
        sec.update()
    else:
        print('Initializing new historical dataset')
        header, table = alphavantage.getHistory(symbol)
        with open(csvPath, 'w') as f:
            wtr = csv.writer(f, lineterminator='\n')
            wtr.writerows([header])
            wtr.writerows(table)
        sec = models.Security(csvPath)
    print('Writing historical data to file')
    sec.save()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Command-line invocation requires a security symbol')
    main(sys.argv[1])

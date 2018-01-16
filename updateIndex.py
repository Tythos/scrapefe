"""Updates security datapoints for each ticker symbol in the given index path.
"""

import csv
import sys
import warnings
from scrapefe import yahoo

def main(indexPath):
    """
    """
    with open(indexPath, 'r') as f:
        dr = csv.DictReader(f)
        rows = [r for r in dr]
    for row in rows:
        symbol = row['symbol']
        print('Pulling and writing %s...' % symbol)
        try:
            result = yahoo.main(symbol)
            with open('data/%s.csv' % symbol, 'w') as f:
                f.write(yahoo.toCsv(result))
        except Exception as e:
            warnings.warn('Unable to parse security %s, skipping...' % symbol)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Requires a path to an index table')
    main(sys.argv[1])

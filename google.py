"""API for Google Finance API
"""

import datetime
import requests
import numpy
from matplotlib import pyplot

def getSecurity(security, index='NASD'):
    """Returns header tuple and [m x n] numpy.array of historical data. It
       appears only one month of historical data is available with the current
       API.
    """
    interval = 86400
    res = requests.get("https://finance.google.com/finance/getprices", params={
        'q': security,
        'x': index,
        'i': str(interval)
    })
    lines = res.content.decode('ascii').splitlines()
    init = 0
    header = ('Date', 'Open', 'High', 'Low', 'Close', 'Volume')
    rows = []
    for price in lines:
        cols = price.split(",")
        if cols[0][0] == 'a':
            init = int(cols[0][1:])
            row = [init, float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])]
            rows.append(row)
        elif cols[0][0].isdigit():
            date = init + (int(cols[0]) * int(interval))
            row = [date, float(cols[4]), float(cols[2]), float(cols[3]), float(cols[1]), int(cols[5])]
            rows.append(row)
    return header, numpy.array(rows)

def main():
    """Grabs and plots Facebook data using getSecurity()
    """
    symbol = 'FB'
    header, table = getSecurity(symbol)
    hf = pyplot.figure()
    hx = hf.add_subplot(111)
    for i in range(1, table.shape[1] - 1):
        hx.plot(table[:, 0], table[:, i])
    hx.legend(header[1:-1])
    hx.set_title('1 Month of %s Price Data' % symbol)
    tickValues = hx.get_xticks()
    tickLabels = []
    for tickValue in tickValues:
        tickLabels.append(datetime.datetime.fromtimestamp(tickValue).strftime('%m/%d'))
    hx.set_xticklabels(tickLabels)
    return hx.figure

if __name__ == "__main__":
    hf = main()
    hf.savefig(__file__.replace('.py', '.png'))

"""
"""

import re
import sys
import json
import bs4
import requests

DEFAULT_BASE_URL = 'https://eresearch.fidelity.com/eresearch/evaluate/fundamentals/keyStatistics.jhtml?stockspage=keyStatistics&symbols='

class ParseError(ValueError):
    """
    """
    pass

def getDollarValue(txt):
    """Input *txt* should be of the format:
         "$(dollar)(optional decimal)(dollar)(magnitude)"
       i.e.,
         "$15.68B" => 1.568e10
    """
    try:
        mags = 'KMBT' # each represents another 3 order of magnitude
        rem = re.search(r"\$(\d+\.?\d*)([" + mags + "])", txt, re.I)
        value = float(rem.groups()[0])
        ndx = mags.index(rem.groups()[1])
        mag = (1 + ndx) * 3
        return value * 10**mag
    except:
        raise ParseError('Unable to parse dollar value from "%s"' % txt)

def getPctlValue(txt):
    """Converts english-suffix percentile expression string into a decimal
       value [0-1]; e.g., "95th" => 0.95
    """
    try:
        val = float(re.search(r"(\d+)", txt).groups()[0])
        return val / 100.
    except:
        raise ParseError('Unable to parse percentile value from "%s"' % txt)

class FundProp(object):
    """Models fundamentals property as captured by "key statistics" page of
       Fidelity security analysis
    """
    
    def __init__(self):
        """
        """
        self.label = ''
        self.compVal = -1
        self.indVal = -1
        self.compPctl = -1

    @classmethod
    def fromRow(cls, tr):
        """
        """
        obj = cls()
        tdi = [td.text for td in tr.find_all('td')]
        obj.label = tdi[0]
        try:
            obj.compVal = getDollarValue(tdi[1].strip())
        except ParseError:
            obj.compVal = '--'
        try:
            obj.indVal = getDollarValue(tdi[2].strip())
        except ParseError:
            obj.indVal = '--'
        try:
            obj.compPctl = getPctlValue(tdi[4].strip())
        except ParseError:
            obj.compPctl = '--'
        return obj

def getUrl(symbol):
    """
    """
    return DEFAULT_BASE_URL + symbol

def getSoup(url):
    """
    """
    res = requests.get(url)
    return bs4.BeautifulSoup(res.content, 'html.parser')

def getName(soup):
    """
    """
    h2 = soup.find('h2', {'id': 'companyName'})
    return h2.text

def getRows(soup):
    """
    """
    rows = []
    tables = soup.find_all('table', {'class': 'datatable-component'})
    for table in tables:
        tri = table.find_all('tr')
        rows = rows + [tr for tr in tri if len(tr.find_all('td')) is 5]
    return rows

def getProps(rows):
    """
    """
    props = []
    for row in rows:
        prop = FundProp.fromRow(row)
        props.append(prop)
    return props
        
def main(symbol):
    """
    """
    url = getUrl(symbol)
    soup = getSoup(url)
    rows = getRows(soup)
    props = getProps(rows)
    return {
        'name': getName(soup),
        'symbol': symbol,
        'props': [p.__dict__ for p in props]
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception('Command-line invocation requires a ticker symbol')
    company = main(sys.argv[1])
    print(json.dumps(company, indent=4))    

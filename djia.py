"""Uses a couple of tools from the *wpse* module to pull the DJIA definition
   from Wikipedia.
"""

from scrapefe import wpse

def main():
    """
    """
    url = 'https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average'
    table = wpse.getWikiTable(url)
    header, entries = wpse.parseTable(table)
    entries = wpse.convertNumberCols(entries)
    return wpse.tableToDicts(header, entries)
    
if __name__ == "__main__":
    print(wpse.writeToCsv(main()))

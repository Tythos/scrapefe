"""
"""

import unittest
from scrapefe import yahoo

class YahooTest(unittest.TestCase):
    """
    """
    
    def test_square(self):
        """
        """
        result = yahoo.main('SQ')
        text = yahoo.toCsv(result)
        with open('sq.csv', 'w') as f:
            f.write(text)
        self.assertTrue(True)
        
if __name__ == "__main__":
    unittest.main()

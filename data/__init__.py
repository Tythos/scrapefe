"""
"""

import os

def getAbsPath():
    """Returns absolute path to the data folder where this module is located
    """
    path, _ = os.path.split(__file__)
    return path

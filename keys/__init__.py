"""
"""

import os

def getAbsPath():
    """
    """
    path, _ = os.path.split(__file__)
    return path

def get(name):
    """
    """
    absPath = getAbsPath() + os.path.sep + name
    with open(absPath, 'r') as f:
        content = f.read()
    return content

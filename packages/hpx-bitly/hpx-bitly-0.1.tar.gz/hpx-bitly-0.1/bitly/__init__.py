from __future__ import absolute_import
from bitly.bitly import Connection, BitlyError, Error
__version__ = '0.1'
__all__ = ["Connection", "BitlyError", "Error"]
__doc__ = """
This is a python library for the bitly api

all methods raise BitlyError on an unexpected response, or a problem with input
format
"""

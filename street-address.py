#!/usr/bin/env python
# Extract street addresses from a text file.

import re
import os.path

class StreetAddress:
  """
    Matches addresses.
  """
  def __init__(self):
    self.number = '(?P<number>\d+)'
    self.streets = '(St(reet|\.?)|L(ane|n\.?)|R(oad|d\.?)|Av(enue|e?\.?)|B(oulevard|lvd\.?))'
    self.partial = self.number + ' (?P<street_name>(\w+ )+?' + self.streets + ')'
    
  def match(self, file):
    """
    Public:
      Extract street addresses from the given file
    
    Parameters:
      file: The file to scan for addresses
    """
    if os.path.exists(file):
      f = open(file, 'r')
      
      for m in re.finditer(self.partial, f.read()):
        yield m.group(0)
    
if __name__ == '__main__':
  import unittest
  
  class TestExtractor(unittest.TestCase):
    def setUp(self):
      self.address = StreetAddress()
      
    def testBadFormat(self):
      ary = []
      for a in self.address.match('samples/bad-formatting.txt'):
        ary.append(a)

      self.assertEqual(ary[0], '9909 Dosah Dr TX 78753')

    def testPenske(self):
      ary = []
      for a in self.address.match('samples/penske.txt'):
        ary.append(a)

      self.assertEqual(ary[0], '1219 W Byron St. #1R Chicago, IL 60613')
  
  unittest.main()
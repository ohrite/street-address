#!/usr/bin/env python
# Extract street addresses from a text file.

import re
import os.path

class StreetAddress:
  """
    Matches addresses.
  """
  def __init__(self):
    self.number = '\d+\s'
    self.streets = '(Dr(ive|\.?)|St(reet|\.?)|L(ane|n\.?)|R(oad|d\.?)|Av(enue|e?\.?)|B(oulevard|lvd\.?))'
    self.suite = '(\s?#.+)?'
    self.partial = self.number + '([A-Za-z\.]+\s)+' + self.suite
    self.city = '(\s\w+,?\s[A-Z]{2}\s[0-9]{5})?'
    self.matcher = self.partial + self.city
    
    print(self.matcher)
    
  def match(self, file):
    """
    Public:
      Extract street addresses from the given file
    
    Parameters:
      file: The file to scan for addresses
    """
    
    if os.path.exists(file):
      f = open(file, 'r')
      content = f.read().replace('\n', ' ')
      
      # print(content)
      
      for m in re.finditer(self.matcher, content):
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
      self.assertEqual(ary[1], '9909 Dorset Austin, TX 78753')

    def testPenske(self):
      ary = []
      for a in self.address.match('samples/penske.txt'):
        ary.append(a)

      self.assertEqual(ary[0], '1219 W Byron St. #1R Chicago, IL 60613')
      self.assertEqual(ary[1], '1033 East 41st Street Chicago, IL 60613')
  
    def testSpelled(self):
      ary = []
      for a in self.address.match('samples/spelled-number.txt'):
        ary.append(a)
        
      self.assertEqual(ary[0], '303 Second St, South Tower, 5th Floor, San Francisco, CA 94107')
  
  unittest.main()
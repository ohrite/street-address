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
    self.streets = '(Dr(ive)?|St(reet)?|L(ane|n)|R(oad|d)|Av(enue|e)|B(oulevard|lvd))'
    self.suite = '(\s#\w+?)?'
    self.with_street = self.number + '(\w+?\s)+?' + self.streets + self.suite
    self.without_street = self.number + '(\w+?\s)+?' + self.streets + '?' + self.suite
    self.city_zip = '(\s\w+?\s[A-Z]{2}\s[0-9]{5})'
    
    print(self.with_street)
    print(self.without_street + self.city_zip)
    
  def match(self, file):
    """
    Public:
      Extract street addresses from the given file
    
    Parameters:
      file: The file to scan for addresses
    """
    result = []
    
    if os.path.exists(file):
      f = open(file, 'r')
      content = re.sub('\s+', ' ', re.sub(',|\.', '', f.read()))


      for m in re.finditer(self.with_street, content):
        result.append(m.group(0))

      for m in re.finditer(self.without_street + self.city_zip, content):
        result.append(m.group(0))
    
    return result
    
if __name__ == '__main__':
  import unittest
  
  class TestExtractor(unittest.TestCase):
    def setUp(self):
      self.address = StreetAddress()

    def testBadFormat(self):
      results = self.address.match('samples/bad-formatting.txt')
      self.assertEqual(len(results), 3)
      self.assertEqual(results, ['9909 Dosah Dr TX 78753',
                                 '9909 Dorset Austin TX 78753',
                                 '3600 Greystone Dr #533 Austin TX 78731'])

    def testChicagoCard(self):
      results = self.address.match('samples/chicago-card.txt')
      self.assertEqual(results, ['1219 W Byron St #1R Chicago IL 60613'])
    
    def testInlineFormats(self):
      results = self.address.match('samples/inline-formats.txt')
      self.assertEqual(results, ['128 E Beaumont St',
                                 '128 East Beaumont Street',
                                 '128 E Bmt St',
                                 '128 Beaumont Street',
                                 '128 Highway 88'])
    
    def testPenske(self):
      results = self.address.match('samples/penske.txt')
      self.assertEqual(results, ['1219 W Byron St 1R Chicago IL 60613',
                                 '1033 East 41st Street Chicago IL 60613'])
      
    def testReceipt(self):
      results = self.address.match('samples/receipt.txt')
      self.assertEqual(results, ['9009 Dorset Dr',
                                 '9009 Dorset Dr Austin TX 78753-4413'])
    
    def testShortForm(self):
      results = self.address.match('samples/short-form.txt')
      self.assertEqual(results, ['9009 Dorset Dr',
                                 '9009 Dorset Dr Austin TX 78753'])
      
    def testSignature(self):
      results = self.address.match('samples/signature.txt')
      self.assertEqual(results, ['1219 W Byron St Rear 1 1R Chicago IL 60613'])
    
    def testSignature2(self):
      results = self.address.match('samples/signature2.txt')
      self.assertEqual(results, ['656 Fifth Ave 20th Floor New York NY 10017'])
      
    def testSpelled(self):
      results = self.address.match('samples/spelled-number.txt')
      self.assertEqual(results, ['303 Second St South Tower 5th Floor San Francisco CA 94107'])

  
  unittest.main()
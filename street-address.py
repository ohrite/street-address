#!/usr/bin/env python
# Extract street addresses from a text file.

import re
import os.path

class StreetAddress:
  def __init__(self):
    self.number = '(?P<number>\d+)'
    self.streets = '(St(reet|\.?)|L(ane|n\.?)|R(oad|d\.?)|Av(enue|e?\.?)|B(oulevard|lvd\.?))'
    self.partial = self.number + ' (?P<street_name>([a-zA-Z]+ )+?' + self.streets + ')'
    
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
  address = StreetAddress()
  for a in address.match('README'):
    print "found: " + a
  
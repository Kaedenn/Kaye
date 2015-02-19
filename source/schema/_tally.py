#!/usr/bin/env python

class Tally(object):
  def __init__(self):
    self._tally = dict()
  
  def tally(self, tile, row, col):
    if not tile in self._tally:
      self._tally[tile] = dict(count = 1, positions = [(row, col)])
    else:
      self._tally[tile]["count"] += 1
      self._tally[tile]["positions"].append((row, col))
  
  def get_count(self, tile):
    if not tile in self._tally:
      return 0
    else:
      return self._tally[tile]["count"]
  
  def get_positions(self, tile):
    if not tile in self._tally:
      return [()]
    else:
      return self._tally[tile]["positions"]


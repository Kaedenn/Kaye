#!/usr/bin/env python

import ctypes

from source.tiles import layers
import random

__all__ = ['LEVEL_ROWS', 'LEVEL_COLS', 'LEVEL_LAYERS', 'Tile', 'Board',
           'Matrix', 'dirs']

LEVEL_ROWS = 32
LEVEL_COLS = 32
LEVEL_LAYERS = len(layers)

Tile = ctypes.c_int
Board = Tile * LEVEL_LAYERS * LEVEL_COLS * LEVEL_ROWS
Matrix = Tile * LEVEL_COLS * LEVEL_ROWS

class _Dir(dict):
  def __init__(self):
    self._dirs = {
      "unknown" : -1,
      "up" : 0,
      "left" : 1,
      "down" : 2,
      "right" : 3
    }
    super(_Dir, self).__init__(**self._dirs)
  
  def __len__(self):
    return len(self._dirs) - 1
  
  def choice(self):
    return random.choice(xrange(len(self)))

dirs = _Dir()


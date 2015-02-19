#!/usr/bin/env python

"""
Encapsulates everything I'd ever want to encapsulate regarding a scheme.

A "scheme" is a format for storing a set of levels at runtime.
A "scheme file" is an XML file from which a scheme can be generated.

The following is a detailed visualization of how a scheme is stored. The
following is assumed:

tile_t is a type that can store a tile number (ctypes.c_int or ctypes.c_long)

scheme = {
  "name" : str,
  "description" : str,
  "msg_win" : str,
  "msg_lose" : str,
  "levels" : [{
    "name" : str,
    "hint" : str,
    "msg_win" : str,
    "msg_lose" : str,
    "tiles" : tile_t[32][32][3],
    "signs" : {
      (int, int) : {
        "once" : bool,
        "sign" : str
      }, ...
    }
  }, ...]
}
"""

from source import errors
from source.schema import nksparser
from source import tiles
from source.tiles import logic, traits
from source import types

def count_diamonds(level):
  diamonds = 0
  for row in level["tiles"]:
    for stack in row:
      for tile in stack:
        if tile == tiles.names["diamond"]:
          diamonds = diamonds + 1
  return diamonds

def grab_level(scheme):
  level = dict()
  level["name"] = scheme["levels"][0]["name"]
  level["hint"] = scheme["levels"][0]["name"]
  level["msg_win"] = scheme["levels"][0]["msg_win"]
  level["msg_lose"] = scheme["levels"][0]["msg_lose"]
  level["tiles"] = types.Board()
  for r, c, l, t in tiles.logic.iterboard(scheme["levels"][0]["tiles"]):
    level["tiles"][r][c][l] = types.Tile(t)
  level["signs"] = dict()
  for sign in scheme["levels"][0]["signs"]:
    level["signs"][sign] = dict()
    level["signs"][sign]["once"] = scheme["levels"][0]["signs"][sign]["once"]
    level["signs"][sign]["sign"] = scheme["levels"][0]["signs"][sign]["sign"]
  return level

def grab_next_level(scheme):
  del scheme["levels"][0]
  if scheme["levels"]:
    return grab_level(scheme)
  else:
    return None

def load(filename):
  parser = nksparser.Parser(filename)
  return parser.get_scheme()


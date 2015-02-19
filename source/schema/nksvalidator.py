#!/usr/bin/env python

from source import errors
from source import tiles
from source import types
from source.schema._tally import Tally

def validate_scheme(filename, scheme):
  if len(scheme["levels"]) == 0:
    raise errors.FileError(filename, "scheme must have at least one level")
  for level in scheme["levels"]:
    validate_level(filename, level)

def validate_level(filename, level):
  def isborder(row, col):
    if row in (0, types.LEVEL_ROWS - 1) or col in (0, types.LEVEL_COLS - 1):
      return True
    return False
  
  # 1) len(levelname) > 0
  if len(level["name"]) == 0:
    raise errors.FileError(filename, "level must have a name")
  # 2) len(hint) > 0
  if len(level["hint"]) == 0:
    raise errors.FileError(filename, "level must have a hint")
  # 3) len(win_msg) > 0
  if len(level["msg_win"]) == 0:
    raise errors.FileError(filename, "level must have a win message")
  # 4) len(lose_msg) > 0
  if len(level["msg_lose"]) == 0:
    raise errors.FileError(filename, "level must have a lose message")
  # 5) begin generation of tally, validate tiles:
  tally = Tally()
  #  a) tile is a known tileid
  for row, col, layer, tile in tiles.logic.iterboard(level["tiles"]):
    #  b) if iswall(row, col): tile == tiles.names["wall_s"]
    if not tile in tiles.tiles:
      raise errors.InvalidTileError(levelname, tile, row, col)
    if isborder(row, col):
      if not tiles.names["wall_s"] in level["tiles"][row][col]:
        raise errors.WallError(levelname, row, col)
    tally.tally(tile, row, col)
  #  c) validate tally
  _validate_tally(level, tally)

def _validate_tally(level, tally):
  if tally.get_count(tiles.names["kye"]) == 0:
    raise errors.MissingKyeError(level["name"])
  elif tally.get_count(tiles.names["kye"]) > 1:
    row, col = tally.get_positions(tiles.names["kye"])[-1]
    raise errors.MultipleKyeError(level["name"], row, col)
  
  if tally.get_count(tiles.names["diamond"]) == 0:
    raise errors.DiamondError(level["name"])
  
  pairs = list()
  pairs.extend(tiles.traits.kyewarpers)
  pairs.extend(tiles.traits.objwarpers)
  
  for tile in pairs:
    if tally.get_count(tile) > 0:
      if tally.get_count(tile) != 2:
        row, col = tally.get_positions(tile)[-1]
        raise errors.TupleError(level["name"], tile, row, col, 2)


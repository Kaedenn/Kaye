#!/usr/bin/env python

from source.tiles.tables import tiles, layers, names
from source import types
from source import errors

def iterboard(board):
  for row in xrange(len(board)):
    for col in xrange(len(board[row])):
      for layer in xrange(len(board[row][col])):
        yield row, col, layer, board[row][col][layer]

def iterlayer():
  yield layers["above"]
  yield layers["normal"]
  yield layers["below"]
  raise StopIteration

letter_to_dir = lambda l: "uldr".find(l)
dir_to_letter = lambda d: "uldr"[d]

def tile_to_dir(tile):
  if hasattr(tile, "partition"):
    return letter_to_dir(tile.partition("_")[-1])
  else:
    return tile_to_dir(tiles[tile]["name"])

def find_kye(board):
  for row, col, layer, tile in iterboard(board):
    if tile == names["kye"]:
      return row, col, layer

def find_tile_pair(board, row, col, tile):
  for r, c, l, t in iterboard(board):
    if t == tile and (r != row or c != col):
      return r, c
  return row, col

def vec(row, col, *args):
  # vec(row, col, dir):
  if len(args) == 1:
    dir = args[0]
    if dir == types.dirs["unknown"]:
      dir = types.dirs.choice()
    return row + (-1, 0, 1, 0)[dir], col + (0, -1, 0, 1)[dir]
  # vec(row, col, torow, tocol):
  elif len(args) == 3:
    targrow, targcol = args[:2]
    normfunc = args[2]
    dr = 0
    dc = 0
    if (targrow - row) ** 2 > (targcol - col) ** 2:
      dr = normfunc(targrow - row)[0]
    else:
      dc = normfunc(targcol - col)[0]
    return row + dr, col + dc

def push_tile(stack, tile):
  if stack[layers["above"]] == names["nothing"]:
    if stack[layers["normal"]] == names["nothing"]:
      if stack[layers["below"]] == names["nothing"]:
        stack[layers["below"]] = tile
      else:
        stack[layers["normal"]] = tile
    else:
      stack[layers["above"]] = tile
  else:
    error = "unable to push tile %s: stack %s is full" % (tile, list(stack))
    raise errors.LogicError(error)

def push_under_tile(stack, tile):
  stack[layers["above"]] = stack[layers["normal"]]
  stack[layers["normal"]] = stack[layers["below"]]
  stack[layers["below"]] = tile

def pop_tile(stack, layer):
  if layer == layers["below"]:
    stack[layers["below"]] = stack[layers["normal"]]
    stack[layers["normal"]] = stack[layers["above"]]
    stack[layers["above"]] = names["nothing"]
  elif layer == layers["normal"]:
    stack[layers["normal"]] = stack[layers["above"]]
    stack[layers["above"]] = names["nothing"]
  elif layer == layers["above"]:
    stack[layers["above"]] = names["nothing"]

def pop_tile_from(stack, tile):
  for i in iterlayer():
    if stack[i] == tile:
      pop_tile(stack, i)

def get_layer(stack, tile):
  for i, t in enumerate(stack):
    if t == tile:
      return i

def reflect_tile(tile):
  tilename = tiles[tile]["name"]
  newdir = (tile_to_dir(tilename) + len(types.dirs) / 2) % len(types.dirs)
  return names[tilename.partition("_")[0] + "_" + dir_to_letter(newdir)]

def redirect_tile(tile, redirector):
  olddir = tile_to_dir(tiles[tile]["name"])
  newdir = tile_to_dir(tiles[redirector]["name"])
  if newdir == -1:
    if tiles[redirector]["name"].partition("_")[-1] == "cw":
      newdir = (olddir - 1) % types.numdirs
    elif tiles[redirector]["name"].partition("_")[-1] == "ccw":
      newdir = (olddir + 1) % types.numdirs
  newname = tiles[tile]["name"].partition("_")[0] + "_" + dir_to_letter(newdir)
  return names[newname]

def get_area_around_tile(level, row, col):
  """
  get_area_around_tile(level, row, col) -> list
  
  Gets a 3x3 area around the specified 'row' and 'col' of the supplied 'level'.
  
  The output of this function will be similar to the following:
  [
    [level[row-1][col-1], level[row-1][col], level[row-1][col+1]],
    [level[row  ][col-1], level[row  ][col], level[row  ][col+1]],
    [level[row+1][col-1], level[row+1][col], level[row+1][col+1]]
  ]
  """
  # thanks to verte for this line...
  l = [cols for rows in level[row-1:row+2] for cols in rows[col-1:col+2]]
  # ...and thanks to yango for this one
  l = [[l[i], l[i+1], l[i+2]] for i in range(0, len(l), 3) if i+2 < len(l)]
  # both from #python on freenode.
  return l

def get_wall_c_bits(area):
  bits = [0, 0, 0, 0]
  '''
  bits:
  [ 0, 0,
    0, 0 ]
  area:
  [ [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0] ]
  '''
  def wall(stack):
    for tile in stack:
      if tile in set((names["wall_s"], names["wall_c"], names["keyed_wall"])):
        return True
    return False
  bits[0] = any(wall(t) for t in (area[0][0], area[1][0], area[0][1]))
  bits[1] = any(wall(t) for t in (area[0][1], area[0][2], area[1][2]))
  bits[2] = any(wall(t) for t in (area[1][2], area[2][2], area[2][1]))
  bits[3] = any(wall(t) for t in (area[1][0], area[2][0], area[2][1]))
  return bits


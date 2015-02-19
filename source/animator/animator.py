#! /usr/bin/env python

"""
Kaye Core Animation and Tile Logic Control

Yeah, I know that's a massive title for this file, but massive tasks deserve
massive titles!

This class (Animator) is responsible for handling all tile interactions in every
senario. This class performs rather complex and intense computation in order to
ensure every tile works the way it's supposed to.

Although a good number of tile behaviors are based on their traits dictionary,
certain "special" tiles are hard-coded to avoid problems with unnecessary levels
of abstraction.

The implementor of this class (currently the Logic controller) needs only to be
concerned with five simple functions:
  anim_timer(self, board)
  anim_up(self, board)
  anim_left(self, board)
  anim_down(self, board)
  anim_right(self, board)
These functions stem from the five possible animation triggers: the timer and
the four arrow keys.

Do note, this module will likely be the bottleneck of the entire program, as it
frequently performs logically intense computations. Optimization may be needed.
"""

import random

from source import events
from source import tiles
from source.tiles import logic
from source.tiles import traits
from source import types

# sometimes I need an ordered intersection, or an intersection of lists
def _intersection(l1, l2):
  return [i for i in l1 if i in l2]

def _normalize(*nums):
  return tuple(i != 0 and i / abs(i) or 0 for i in nums)

_drdc = { }
_drdc["rocky"] = {
  "test" : (
    ((0, 0), (-1, 1), (0, 0), (1, -1)),
    ((-1, 1), (0, 0), (-1, 1), (0, 0))
  ),
  "go" : (
    ((-1, -1), (-1, 1), (1, 1), (1, -1)),
    ((-1, 1), (-1, -1), (-1, 1), (1, 1))
  )
}
_drdc["magnet"] = {
  "h" : ((0, -2), (0, -1), (0, 2), (0, 1)),
  "v" : ((-2, 0), (-1, 0), (2, 0), (1, 0))
}
_drdc["tnt"] = (
  (-1, -1), (-1, 0), (-1, 1),
  (0, -1), (0, 0), (0, 1),
  (1, -1), (1, 0), (1, 1)
)

class Animator(object):
  
  RES_NO_EVENT = 0
  RES_FOUND_DIAMOND = 1
  RES_FOUND_SIGN = 1 << 1
  
  def __init__(self):
    # frame constants assume ticks occur every 1/4 second
    self._frame = 0
    self._frames = 4
    self._fps = self._frames
    self._every_second = lambda frame: frame % self._fps == 0
    self._every_half_second = lambda frame: frame % self._fps / 2 == 0
    self._every_quarter_second = lambda frame: frame % self._fps / 4 == 0
    self._counter = 0
    self._countmax = self._frames
    self._signlocs = ()
  
  def inform(self, signs):
    self._signlocs = signs.keys()
  
  def _begin_anim(self, board):
    self._animatrix = types.Matrix()
    self._kyepos = logic.find_kye(board)
  
  def _move_kye_to(self, board, row, col, layer, dir):
    torow, tocol = logic.vec(row, col, dir)
    tostack = board[torow][tocol]
    canmove = False
    event = 0
    if traits.passable_kye(tostack):
      canmove = True
      if tiles.names["diamond"] in tostack:
        # found a diamond!
        logic.pop_tile_from(tostack, tiles.names["diamond"])
        event |= self.RES_FOUND_DIAMOND
      elif tiles.names["food"] in tostack:
        logic.pop_tile_from(tostack, tiles.names["food"])
      elif traits.hazard(tostack):
        # kye dies here
        raise events.KyeKilledEvent()
      elif _intersection(tostack, traits.kyewarpers):
        # warp the kye
        warper = _intersection(tostack, traits.kyewarpers)[0]
        # canmove == False because we're going to move kye for him
        canmove = False
        # find other warper: is it covered?
        warprow, warpcol = logic.find_tile_pair(board, torow, tocol, warper)
        # if not, warp the little guy
        if warprow != row or warpcol != col:
          warpstack = board[warprow][warpcol]
          if not traits.covered(warpstack, logic.get_layer(warpstack, warper)):
            logic.pop_tile(board[row][col], layer)
            logic.push_tile(board[warprow][warpcol], tiles.names["kye"])
            if (warprow, warpcol) in self._signlocs:
              event |= self.RES_FOUND_SIGN
          else:
            canmove = True
        else:
          canmove = True
      elif tiles.names["plunger"] in tostack:
        # explode all TNT
        for r, c, l, t in logic.iterboard(board):
          if t in traits.tnts:
            self._explode(board, r, c)
          elif t == tiles.names["plunger"]:
            logic.pop_tile(board[r][c], l)
      elif tiles.names["key"] in tostack:
        # handle the key event
        for r, c, l, t in logic.iterboard(board):
          if t in traits.keyed:
            logic.pop_tile(board[r][c], l)
    elif traits.pushable_kye(tostack):
      # push an object
      if self._handle_push(board, torow, tocol, dir):
        canmove = True
    if canmove:
      logic.pop_tile(board[row][col], layer)
      logic.push_tile(tostack, tiles.names["kye"])
      if (torow, tocol) in self._signlocs:
        event |= self.RES_FOUND_SIGN
    for orient, drdc in _drdc["magnet"].iteritems():
      for r, c in drdc:
        if any((torow + r not in xrange(types.LEVEL_ROWS),
                tocol + c not in xrange(types.LEVEL_COLS))):
          continue
        magstack = board[torow + r][tocol + c]
        if _intersection(magstack, traits.magnets):
          magnet = _intersection(magstack, traits.magnets)[0]
          if tiles.tiles[magnet]["name"][-1] == orient:
            dr, dc = _normalize(r, c)
            layer = logic.get_layer(magstack, magnet)
            if r != dr or c != dc:
              pos = (torow + r, tocol + c, layer, torow + dr, tocol + dc)
              if self._move_obj_to(board, *pos):
                self._handle_magnet(board, torow + dr, tocol + dc, orient)
    return event
  
  def _move_obj_to(self, board, row, col, layer, torow, tocol):
    tile = board[row][col][layer]
    if self._place_obj_at(board, torow, tocol, tile):
      logic.pop_tile(board[row][col], layer)
      return True
    return False
  
  def _place_obj_at(self, board, row, col, tile):
    if traits.passable_obj(board[row][col]):
      if traits.destructive(board[row][col]):
        # do nothing, because return True will make the object vanish
        pass
      elif _intersection(board[row][col], traits.objwarpers):
        # find the other objwarper
        totile = _intersection(board[row][col], traits.objwarpers)[0]
        warprow, warpcol = logic.find_tile_pair(board, row, col, tile)
        if warprow != row or warpcol != col:
          logic.push_tile(board[warprow][warpcol], tile)
          self._animatrix[warprow][warpcol] = True
      else:
        logic.push_tile(board[row][col], tile)
      return True
    return False
  
  def _scan_for_magnet(self, board, row, col):
    for orient in set(["h", "v"]):
      for r, c in _drdc["magnet"][orient]:
        if tiles.names["magnet_" + orient] in board[row + r][col + c]:
          return (r, c)
    return False
  
  def _handle_bouncer(self, board, row, col, layer):
    if self._scan_for_magnet(board, row, col):
      return
    tile = board[row][col][layer]
    tilename = tiles.tiles[tile]["name"]
    dir = logic.letter_to_dir(tilename[-1])
    torow, tocol = logic.vec(row, col, dir)
    tostack = board[torow][tocol]
    if self._move_obj_to(board, row, col, layer, torow, tocol):
      self._animatrix[torow][tocol] = True
    elif traits.redirector(tostack):
      redirector = _intersection(tostack, traits.redirectors)[0]
      board[row][col][layer] = logic.redirect_tile(tile, redirector)
    elif tiles.names["tnt_u"] in tostack:
      self._explode(board, torow, tocol)
    else:
      newtile = logic.reflect_tile(board[row][col][layer])
      if traits.pushable_obj(tostack):
        self._handle_bump(board, torow, tocol, dir)
      board[row][col][layer] = newtile
    self._animatrix[row][col] = True
  
  def _handle_rocky(self, board, row, col, layer):
    if self._scan_for_magnet(board, row, col):
      return
    tile = board[row][col][layer]
    tilename = tiles.tiles[tile]["name"]
    dir = logic.letter_to_dir(tilename[-1])
    torow, tocol = logic.vec(row, col, dir)
    tostack = board[torow][tocol]
    if self._move_obj_to(board, row, col, layer, torow, tocol):
      self._animatrix[torow][tocol] = True
    elif traits.circular(tostack) and not traits.surrounded(board, row, col):
      for i in (0, 1):
        testr = row + _drdc["rocky"]["test"][0][dir][i]
        testc = col + _drdc["rocky"]["test"][1][dir][i]
        torow = row + _drdc["rocky"]["go"][0][dir][i]
        tocol = col + _drdc["rocky"]["go"][1][dir][i]
        if traits.passable_obj(board[testr][testc]):
          if self._move_obj_to(board, row, col, layer, torow, tocol):
            self._animatrix[torow][tocol] = True
    elif traits.redirector(tostack):
      redirector = _intersection(tostack, traits.redirectors)[0]
      board[row][col][layer] = logic.redirect_tile(tile, redirector)
    self._animatrix[row][col] = True
  
  def _handle_monster(self, board, row, col, layer):
    if self._scan_for_magnet(board, row, col):
      return
    # try to move towards kye
    moved = False
    kr, kc, kl = self._kyepos
    newrow, newcol = logic.vec(row, col, kr, kc, _normalize)
    if not self._animatrix[newrow][newcol]:
      if self._move_obj_to(board, row, col, layer, newrow, newcol):
        self._animatrix[newrow][newcol] = True
        moved = True
    # if that didn't work (we're blocked), move randomly
    if not moved:
      dirs = types.dirs.values()
      random.shuffle(dirs)
      for dir in dirs:
        newrow, newcol = logic.vec(row, col, dir)
        if not self._animatrix[newrow][newcol]:
          if self._move_obj_to(board, row, col, layer, newrow, newcol):
            self._animatrix[newrow][newcol] = True
            break
    self._animatrix[row][col] = True
  
  def _handle_box(self, board, row, col, layer):
    tile = board[row][col][layer]
    tilename = tiles.tiles[tile]["name"]
    newrow, newcol = logic.vec(row, col, logic.letter_to_dir(tilename[-1]))
    if tilename[:-2] == "rockybox":
      newtile = tiles.names["rocky_" + tilename[-1]]
    elif tilename == "monsterbox":
      newtile = random.choice(traits.monsters)
    if traits.passable_obj(board[newrow][newcol]):
      self._place_obj_at(board, newrow, newcol, newtile)
      self._animatrix[newrow][newcol] = True
  
  def _handle_chronomorph(self, board, row, col, layer):
    tile = board[row][col][layer]
    trait = lambda tile, trait: traits.traits[tile][trait]
    newtile = tiles.names[trait(tile, "chronomorphic")[1]]
    if not traits.covered(board[row][col], layer):
      board[row][col][layer] = newtile
    if trait(newtile, "hazard")[0] or trait(newtile, "destructive"):
      if tiles.names["kye"] in board[row][col]:
        raise events.KyeKilledEvent()
  
  def _handle_push(self, board, row, col, dir):
    pushable = lambda t: traits.traits[t]["pushable"][0]
    targrow, targcol = logic.vec(row, col, dir)
    for l in logic.iterlayer():
      if pushable(board[row][col][l]):
        layer = l
        break
    if self._move_obj_to(board, row, col, layer, targrow, targcol):
      dmdx = self._scan_for_magnet(board, targrow, targcol)
      if dmdx:
        self._handle_magnet(board, targrow + dmdx[0], targcol + dmdx[1])
      return True
    return False
  
  def _handle_bump(self, board, row, col, dir):
    pushable = lambda t: traits.traits[t]["pushable"][1]
    newrow, newcol = logic.vec(row, col, dir)
    for l in logic.iterlayer():
      if pushable(board[row][col][l]):
        layer = l
        break
    if self._scan_for_magnet(board, row, col):
      return False
    if self._move_obj_to(board, row, col, layer, newrow, newcol):
      dmdx = self._scan_for_magnet(board, newrow, newcol)
      if dmdx:
        self._handle_magnet(board, newrow + dmdx[0], newcol + dmdx[1])
      self._animatrix[newrow][newcol] = True
    self._animatrix[row][col] = True
  
  def _handle_magnet(self, board, row, col, orient = None):
    if orient is None:
      tile = _intersection(board[row][col], traits.magnets)[0]
      orient = tiles.tiles[tile]["name"][-1]
    for r, c in _drdc["magnet"][orient]:
      for l in logic.iterlayer():
        # case where board[...] == tiles.names["kye"] is handled within the
        # _move_kye_to method
        if board[row + r][col + c][l] != tiles.names["kye"]:
          if traits.traits[board[row + r][col + c][l]]["magnetic"]:
            dr, dc = _normalize(r, c)
            torow = row + dr
            tocol = col + dc
            if self._move_obj_to(board, row + r, col + c, l, torow, tocol):
              self._animatrix[torow][tocol] = True
  
  def _handle_explosion(self, board, row, col, layer):
    logic.pop_tile(board[row][col], layer)
    logic.push_under_tile(board[row][col], tiles.names["burnt"])
  
  def _explode(self, board, row, col):
    place = False
    for layer, tile in enumerate(board[row][col]):
      if tile == tiles.names["nothing"]:
        if layer != tiles.tiles[tiles.names["nothing"]]["layer"]:
          continue
        place = True
      elif tile == tiles.names["kye"]:
        # oh boy
        raise events.KyeKilledEvent()
      elif tile in traits.tnts:
        # found TNT at explosion site
        logic.pop_tile(board[row][col], layer)
        for r, c in _drdc["tnt"]:
          self._explode(board, row + r, col + c)
        place = True
      elif traits.traits[tile]["destructible"]:
        logic.pop_tile(board[row][col], layer)
        place = True
    if place:
      if not tiles.names["explosion"] in board[row][col]:
        logic.push_tile(board[row][col], tiles.names["explosion"])
      self._animatrix[row][col] = True
  
  def _anim_kye_move(self, board, dir):
    row, col, layer = logic.find_kye(board)
    # following line can either:
    #  return RES_FOUND_DIAMOND
    #  return RES_FOUND_SIGN
    # or any bitwise combination thereof
    retcode = self._move_kye_to(board, row, col, layer, dir)
    for r in xrange(row - 1, row + 2):
      for c in xrange(col - 1, col + 2):
        if traits.area_hazard(board[r][c]):
          # eh I'll give the player a break
          if not retcode & self.RES_FOUND_DIAMOND:
            raise events.KyeKilledEvent()
    return retcode
  
  def anim_timer(self, board):
    self._frame = (self._frame + 1) % self._frames
    self._begin_anim(board)
    for row, col, layer, tile in logic.iterboard(board):
      if self._animatrix[row][col]:
        continue
      if self._every_second(self._frame):
        if traits.traits[tile]["chronomorphic"][0]:
          self._handle_chronomorph(board, row, col, layer)
        if tile in traits.bouncers:
          self._handle_bouncer(board, row, col, layer)
      if self._every_half_second(self._frame):
        if tile in traits.boxes:
          self._handle_box(board, row, col, layer)
        elif tile in traits.monsters:
          self._handle_monster(board, row, col, layer)
        elif tiles.tiles[tile]["name"] == "explosion":
          self._handle_explosion(board, row, col, layer)
      if self._every_quarter_second(self._frame):
        if not self._animatrix[row][col]:
          if tile in traits.rockies:
            if not self._animatrix[row][col]:
              self._handle_rocky(board, row, col, layer)
          elif tile in traits.magnets:
            orient = tiles.tiles[tile]["name"][-1]
            self._handle_magnet(board, row, col, orient)
  
  def anim_up(self, board):
    return self._anim_kye_move(board, types.dirs["up"])
  
  def anim_left(self, board):
    return self._anim_kye_move(board, types.dirs["left"])
  
  def anim_down(self, board):
    return self._anim_kye_move(board, types.dirs["down"])
  
  def anim_right(self, board):
    return self._anim_kye_move(board, types.dirs["right"])
  

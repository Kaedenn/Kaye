#!/usr/bin/env python

from source.tiles import tables

traits = {}

_mktup = lambda *a: tuple(tables.names[t] for t in a)

monsters = _mktup("spikey", "chompy", "pokey", "squeakie", "sharkie")
rockies = _mktup("rocky_u", "rocky_l", "rocky_d", "rocky_r")
bouncers = _mktup("bouncer_u", "bouncer_l", "bouncer_d", "bouncer_r")
magnets = _mktup("magnet_h", "magnet_v")
boxes = _mktup("rockybox_u", "rockybox_l", "rockybox_d", "rockybox_r",
               "monsterbox")
kyewarpers = _mktup("kyewarper_0", "kyewarper_1", "kyewarper_2", "kyewarper_3",
                    "kyewarper_4", "kyewarper_5", "kyewarper_6", "kyewarper_7",
                    "kyewarper_8", "kyewarper_9", "kyewarper_10",
                    "kyewarper_11", "kyewarper_12", "kyewarper_13",
                    "kyewarper_14", "kyewarper_15")
objwarpers = _mktup("objwarper_0", "objwarper_1", "objwarper_2", "objwarper_3",
                    "objwarper_4", "objwarper_5", "objwarper_6", "objwarper_7",
                    "objwarper_8", "objwarper_9", "objwarper_10",
                    "objwarper_11", "objwarper_12", "objwarper_13",
                    "objwarper_14", "objwarper_15")
redirectors = _mktup("redirector_u", "redirector_l", "redirector_d",
                     "redirector_r", "redirector_cw", "redirector_ccw")
tnts = _mktup("tnt_u", "tnt_s")
#keyed = _mktup("lazer_h", "lazer_v")
keyed = _mktup("keyed_wall")

def covered(stack, layer = tables.layers["above"]):
  def iscover(tile):
    if False in traits[tile]["passable"]:
      # kye can't be considered a cover
      if tile != tables.names["kye"]:
        return True
    return False
  
  if layer == tables.layers["above"]:
    return False
  elif layer == tables.layers["normal"]:
    return iscover(stack[tables.layers["above"]])
  elif layer == tables.layers["below"]:
    return True in (
      iscover(stack[tables.layers["normal"]]),
      iscover(stack[tables.layers["above"]])
    )
  return False

def surrounded(board, row, col):
  drdc = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
  for r, c in drdc:
    if passable_obj(board[row + r][row + c]):
      return False
  return True

def blocking(stack):
  return not passable_kye(stack) and not passable_obj(stack)

def passable_kye(stack):
  if traits[stack[tables.layers["above"]]]["passable"][0] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][0] == True:
      if traits[stack[tables.layers["below"]]]["passable"][0] == True:
        return True
  return False

def passable_obj(stack):
  if traits[stack[tables.layers["above"]]]["passable"][1] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][1] == True:
      if traits[stack[tables.layers["below"]]]["passable"][1] == True:
        return True
  return False

def hazard(stack):
  if destructive(stack):
    return True
  if traits[stack[tables.layers["above"]]]["hazard"][0] == True:
    return True
  if traits[stack[tables.layers["normal"]]]["hazard"][0] == True:
    return True
  if traits[stack[tables.layers["below"]]]["hazard"][0] == True:
    return True
  return False

def area_hazard(stack):
  if traits[stack[tables.layers["above"]]]["hazard"][1] == True:
    return True
  if traits[stack[tables.layers["normal"]]]["hazard"][1] == True:
    return True
  if traits[stack[tables.layers["below"]]]["hazard"][1] == True:
    return True
  return False

def destructive(stack):
  if traits[stack[tables.layers["above"]]]["destructive"] == True:
    return True
  if traits[stack[tables.layers["normal"]]]["destructive"] == True:
    return True
  if traits[stack[tables.layers["below"]]]["destructive"] == True:
    return True
  return False

def destructible(stack):
  if traits[stack[tables.layers["above"]]]["destructible"] == True:
    if traits[stack[tables.layers["normal"]]]["destructible"] == True:
      if traits[stack[tables.layers["below"]]]["destructible"] == True:
        return True
  return False

def pushable_kye(stack):
  if traits[stack[tables.layers["above"]]]["pushable"][0] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][0] == True:
      if traits[stack[tables.layers["below"]]]["passable"][0] == True:
        return True
  if traits[stack[tables.layers["above"]]]["passable"][0] == True:
    if traits[stack[tables.layers["normal"]]]["pushable"][0] == True:
      if traits[stack[tables.layers["below"]]]["passable"][0] == True:
        return True
  if traits[stack[tables.layers["above"]]]["passable"][0] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][0] == True:
      if traits[stack[tables.layers["below"]]]["pushable"][0] == True:
        return True
  return False

def pushable_obj(stack):
  if traits[stack[tables.layers["above"]]]["pushable"][1] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][1] == True:
      if traits[stack[tables.layers["below"]]]["passable"][1] == True:
        return True
  if traits[stack[tables.layers["above"]]]["passable"][1] == True:
    if traits[stack[tables.layers["normal"]]]["pushable"][1] == True:
      if traits[stack[tables.layers["below"]]]["passable"][1] == True:
        return True
  if traits[stack[tables.layers["above"]]]["passable"][1] == True:
    if traits[stack[tables.layers["normal"]]]["passable"][1] == True:
      if traits[stack[tables.layers["below"]]]["pushable"][1] == True:
        return True
  return False

def magnetic(stack):
  if traits[stack[tables.layers["above"]]]["magnetic"] == True:
    return True
  if traits[stack[tables.layers["normal"]]]["magnetic"] == True:
    return True
  if traits[stack[tables.layers["below"]]]["magnetic"] == True:
    return True
  return False

def circular(stack):
  if traits[stack[tables.layers["above"]]]["circular"] == True:
    return True
  if traits[stack[tables.layers["normal"]]]["circular"] == True:
    return True
  if traits[stack[tables.layers["below"]]]["circular"] == True:
    return True
  return False

def redirector(stack):
  for t in stack:
    if t in redirectors:
      if not covered(stack):
        return True
  return False

traits[tables.names["nothing"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kye"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["life"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["diamond"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["wall_s"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["wall_c"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["burnt"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["food"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["block_s"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["block_c"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["bouncer_u"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["bouncer_l"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["bouncer_d"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["bouncer_r"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["rocky_u"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["rocky_l"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["rocky_d"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["rocky_r"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : True,
  "chronomorphic" : (False, None)
}

traits[tables.names["magnet_h"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["magnet_v"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["gravity_d"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["gravity_u"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["plunger"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["key"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["spikes"]] = {
  "passable" : (True, False),
  "hazard" : (True, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "spikes_r")
}

traits[tables.names["spikes_r"]] = {
  "passable" : (True, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "spikes")
}

traits[tables.names["lava"]] = {
  "passable" : (True, True),
  "hazard" : (True, False),
  "destructive" : True,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["blackhole"]] = {
  "passable" : (True, True),
  "hazard" : (True, False),
  "destructive" : True,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["keyed_wall"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : False,
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : False
}

#traits[tables.names["lazer_h"]] = {
#  "passable" : (True, True),
#  "hazard" : (True, False),
#  "destructive" : True,
#  "destructible" : False,
#  "pushable" : (False, False),
#  "magnetic" : False,
#  "circular" : False,
#  "chronomorphic" : (False, None)
#}

#traits[tables.names["lazer_v"]] = {
#  "passable" : (True, True),
#  "hazard" : (True, False),
#  "destructive" : True,
#  "destructible" : False,
#  "pushable" : (False, False),
#  "magnetic" : False,
#  "circular" : False,
#  "chronomorphic" : (False, None)
#}

traits[tables.names["spikey"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["chompy"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["pokey"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["squeakie"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["sharkie"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : True,
  "pushable" : (False, True),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["explosion"]] = {
  "passable" : (True, True),
  "hazard" : (True, False),
  "destructive" : True,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "burnt")
}

traits[tables.names["tnt_u"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["tnt_s"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["rockybox_u"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["rockybox_l"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["rockybox_d"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["rockybox_r"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["monsterbox"]] = {
  "passable" : (False, False),
  "hazard" : (True, True),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_u"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_l"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_d"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_r"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_ccw"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["redirector_cw"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (True, False),
  "magnetic" : True,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["counter_0"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "nothing")
}

traits[tables.names["counter_1"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_0")
}

traits[tables.names["counter_2"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_1")
}

traits[tables.names["counter_3"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_2")
}

traits[tables.names["counter_4"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_3")
}

traits[tables.names["counter_5"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_4")
}

traits[tables.names["counter_6"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_5")
}

traits[tables.names["counter_7"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_6")
}

traits[tables.names["counter_8"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_7")
}

traits[tables.names["counter_9"]] = {
  "passable" : (False, False),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (True, "counter_8")
}

traits[tables.names["objwarper_0"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_1"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_2"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_3"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_4"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_5"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_6"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_7"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_8"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["objwarper_9"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_0"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_1"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_2"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_3"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_4"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_5"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_6"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_7"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_8"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_9"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_10"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_11"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_12"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_13"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_14"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}

traits[tables.names["kyewarper_15"]] = {
  "passable" : (True, True),
  "hazard" : (False, False),
  "destructive" : False,
  "destructible" : False,
  "pushable" : (False, False),
  "magnetic" : False,
  "circular" : False,
  "chronomorphic" : (False, None)
}


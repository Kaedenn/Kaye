#!/usr/bin/env python

# id -> attributes...
tiles = {}
# name -> id
names = {}

layers = {
  "below" : 0,
  "normal" : 1,
  "above" : 2,
}

def _gentile(name, id, layer):
  tiles[id] = {
    "name" : name,
    "layer" : layer
  }
  names[name] = id

_gentile("nothing", 0x00, layers["below"])
_gentile("kye", 0x01, layers["normal"])
_gentile("life", 0x02, layers["normal"])
_gentile("diamond", 0x03, layers["normal"])
_gentile("wall_s", 0x04, layers["normal"])
_gentile("wall_c", 0x05, layers["normal"])
_gentile("burnt", 0x06, layers["below"])
_gentile("food", 0x10, layers["normal"])
_gentile("block_s", 0x11, layers["normal"])
_gentile("block_c", 0x12, layers["normal"])
_gentile("bouncer_u", 0x13, layers["normal"])
_gentile("bouncer_l", 0x14, layers["normal"])
_gentile("bouncer_d", 0x15, layers["normal"])
_gentile("bouncer_r", 0x16, layers["normal"])
_gentile("rocky_u", 0x17, layers["normal"])
_gentile("rocky_l", 0x18, layers["normal"])
_gentile("rocky_d", 0x19, layers["normal"])
_gentile("rocky_r", 0x1a, layers["normal"])
_gentile("magnet_h", 0x20, layers["normal"])
_gentile("magnet_v", 0x21, layers["normal"])
_gentile("gravity_d", 0x22, layers["below"])
_gentile("gravity_u", 0x23, layers["below"])
_gentile("plunger", 0x24, layers["normal"])
_gentile("key", 0x25, layers["normal"])
_gentile("spikes", 0x30, layers["below"])
_gentile("spikes_r", 0x31, layers["below"])
_gentile("lava", 0x32, layers["below"])
_gentile("blackhole", 0x33, layers["below"])
_gentile("keyed_wall", 0x34, layers["normal"])
#_gentile("lazer_h", 0x34, layers["normal"])
#_gentile("lazer_v", 0x35, layers["normal"])
_gentile("spikey", 0x36, layers["normal"])
_gentile("chompy", 0x37, layers["normal"])
_gentile("pokey", 0x38, layers["normal"])
_gentile("squeakie", 0x39, layers["normal"])
_gentile("sharkie", 0x3a, layers["normal"])
_gentile("explosion", 0x3b, layers["normal"])
_gentile("tnt_u", 0x3c, layers["normal"])
_gentile("tnt_s", 0x3d, layers["normal"])
_gentile("rockybox_u", 0x40, layers["normal"])
_gentile("rockybox_l", 0x41, layers["normal"])
_gentile("rockybox_d", 0x42, layers["normal"])
_gentile("rockybox_r", 0x43, layers["normal"])
_gentile("monsterbox", 0x44, layers["normal"])
_gentile("redirector_u", 0x50, layers["normal"])
_gentile("redirector_l", 0x51, layers["normal"])
_gentile("redirector_d", 0x52, layers["normal"])
_gentile("redirector_r", 0x53, layers["normal"])
_gentile("redirector_ccw", 0x54, layers["normal"])
_gentile("redirector_cw", 0x55, layers["normal"])
_gentile("counter_0", 0x70, layers["normal"])
_gentile("counter_1", 0x71, layers["normal"])
_gentile("counter_2", 0x72, layers["normal"])
_gentile("counter_3", 0x73, layers["normal"])
_gentile("counter_4", 0x74, layers["normal"])
_gentile("counter_5", 0x75, layers["normal"])
_gentile("counter_6", 0x76, layers["normal"])
_gentile("counter_7", 0x77, layers["normal"])
_gentile("counter_8", 0x78, layers["normal"])
_gentile("counter_9", 0x79, layers["normal"])
#_gentile("counter_10", 0x7a, layers["normal"])
#_gentile("counter_11", 0x7b, layers["normal"])
#_gentile("counter_12", 0x7c, layers["normal"])
#_gentile("counter_13", 0x7d, layers["normal"])
#_gentile("counter_14", 0x7e, layers["normal"])
#_gentile("counter_15", 0x7f, layers["normal"])
_gentile("objwarper_0", 0x80, layers["below"])
_gentile("objwarper_1", 0x81, layers["below"])
_gentile("objwarper_2", 0x82, layers["below"])
_gentile("objwarper_3", 0x83, layers["below"])
_gentile("objwarper_4", 0x84, layers["below"])
_gentile("objwarper_5", 0x85, layers["below"])
_gentile("objwarper_6", 0x86, layers["below"])
_gentile("objwarper_7", 0x87, layers["below"])
_gentile("objwarper_8", 0x88, layers["below"])
_gentile("objwarper_9", 0x89, layers["below"])
_gentile("objwarper_10", 0x8a, layers["below"])
_gentile("objwarper_11", 0x8b, layers["below"])
_gentile("objwarper_12", 0x8c, layers["below"])
_gentile("objwarper_13", 0x8d, layers["below"])
_gentile("objwarper_14", 0x8e, layers["below"])
_gentile("objwarper_15", 0x8f, layers["below"])
_gentile("kyewarper_0", 0x90, layers["below"])
_gentile("kyewarper_1", 0x91, layers["below"])
_gentile("kyewarper_2", 0x92, layers["below"])
_gentile("kyewarper_3", 0x93, layers["below"])
_gentile("kyewarper_4", 0x94, layers["below"])
_gentile("kyewarper_5", 0x95, layers["below"])
_gentile("kyewarper_6", 0x96, layers["below"])
_gentile("kyewarper_7", 0x97, layers["below"])
_gentile("kyewarper_8", 0x98, layers["below"])
_gentile("kyewarper_9", 0x99, layers["below"])
_gentile("kyewarper_10", 0x9a, layers["below"])
_gentile("kyewarper_11", 0x9b, layers["below"])
_gentile("kyewarper_12", 0x9c, layers["below"])
_gentile("kyewarper_13", 0x9d, layers["below"])
_gentile("kyewarper_14", 0x9e, layers["below"])
_gentile("kyewarper_15", 0x9f, layers["below"])


#!/usr/bin/env python

"""
Proper ways to get to things from external modules:

source.tiles.tiles
source.tiles.names
source.tiles.layers
source.tiles.logic
source.tiles.traits

there are two ways to get to the first three things:
source.tiles.tables.*
source.tiles.*

TODO: make the source.tiles.tables module private

"""
from source.tiles.tables import tiles, names, layers
from source.tiles import logic
from source.tiles import traits


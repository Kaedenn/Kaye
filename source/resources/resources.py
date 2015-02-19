#!/usr/bin/env python

import gtk
import gobject
import os.path
import sys

from source import errors
from source import path
from source import tiles
from source import types
from source import xpmdata

TILE_SIZE = (16, 16)
BOARD_SIZE = (TILE_SIZE[0] * types.LEVEL_ROWS, TILE_SIZE[1] * types.LEVEL_COLS)

class Drawer(object):
  
  def __init__(self, area, tile_images, splash_image, sign_image):
    self._area = area
    self._tiles = tile_images
    self._splash = splash_image
    self._sign = sign_image
    
    self._gc = self._area.new_gc()
    self._colormap = gtk.gdk.Colormap(gtk.gdk.visual_get_system(), False)
    white = self._colormap.alloc_color("#FFFFFF")
    self._gc.set_foreground(white)
    self._gc.set_background(white)
    
    # one for each layer, one for the splash, and one for the signs
    self._back_buffers = [0] * (types.LEVEL_LAYERS + 2)
    for buff in xrange(len(self._back_buffers)):
      self._back_buffers[buff] = gtk.gdk.Pixmap(self._area,
                                                *self._area.get_size())
    
    self._tile_cache = types.Board()
    self._rctopx = lambda r, c: (c * TILE_SIZE[1], r * TILE_SIZE[0])
    
    for buff in self._back_buffers:
      buff.draw_rectangle(self._gc, True, 0, 0, BOARD_SIZE[1], BOARD_SIZE[0])
  
  def _clear_buffer_at(self, buff, row, col):
    buff.draw_rectangle(self._gc, True, *(self._rctopx(row, col) + TILE_SIZE))
  
  def _draw_tile(self, buff, tile, row, col, *args):
    if self._tiles[tile] is None:
      # no use drawing tiles for which there is no image
      return
    if tile == tiles.names["wall_c"]:
      # we have a circular wall here!
      pos = (
        (0,                0),
        (TILE_SIZE[0] / 2, 0),
        (TILE_SIZE[0] / 2, TILE_SIZE[1] / 2),
        (0,                TILE_SIZE[1] / 2)
      )
      exts = (TILE_SIZE[0] / 2, TILE_SIZE[1] / 2)
      bits = args[0]
      wall_s = self._tiles[tiles.names["wall_s"]]
      wall_c = self._tiles[tiles.names["wall_c"]]
      offset = self._rctopx(row, col)
      for bits in xrange(len(bits)):
        sx, sy = pos[bit]
        dx, dy = offset[0] + sx, offset[1] + sy
        w, h = exts
        if bits[bit]:
          buff.draw_pixbuf(self._gc, wall_s, sx, sy, dx, dy, w, h)
        else:
          buff.draw_pixbuf(self._gc, wall_c, sx, sy, dx, dy, w, h)
    else:
      pos = self._rctopx(row, col)
      buff.draw_pixbuf(self._gc, self._tiles[tile], 0, 0, *pos)
  
  def render_splash(self):
    self._back_buffers[-1].draw_pixbuf(self._gc, self._splash, 0, 0, 0, 0)
    self._area.invalidate_rect((0, 0) + self._area.get_size(), False)
  
  def render_tiles(self, level):
    """render(self) -> None
    
    Draws all the tiles and other images to the internal buffer(s).
    """
    
    region = gtk.gdk.Region()
    for row, col, layer, tile in tiles.logic.iterboard(level):
      if tile != self._tile_cache[row][col][layer]:
        # different tile: update the cache and draw it
        region.union_with_rect(self._rctopx(row, col) + TILE_SIZE)
        self._tile_cache[row][col][layer] = tile
        if tiles.tiles[tile]["name"] == "nothing":
          self._clear_buffer_at(self._back_buffers[layer], row, col)
        elif tiles.tiles[tile]["name"] == "wall_c":
          # circular walls have a custom drawing algorithm
          area = tiles.logic.get_area_around_tile(level, row, col)
          corners = tiles.logic.get_wall_c_bits(area)
          self._draw_tile(self._back_buffers[layer], tile, row, col, corners)
        else:
          self._draw_tile(self._back_buffers[layer], tile, row, col)
    if not region.empty():
      self._area.invalidate_region(region, True)
  
  def render_signs(self, signs):
    buff = self._back_buffers[-2]
    buff.draw_rectangle(self._gc, True, 0, 0, BOARD_SIZE[1], BOARD_SIZE[0])
    for row, col in signs:
      pos = self._rctopx(row, col)
      buff.draw_pixbuf(self._gc, self._sign, 0, 0, *pos)
  
  def render_to_area(self, splash = False):
    posext = (0, 0, 0, 0, -1, -1)
    if splash:
      # draw the splash image
      self._area.draw_drawable(self._gc, self._back_buffers[-1], *posext)
    else:
      # otherwise, draw the tiles with transparency
      self._area.draw_drawable(self._gc, self._back_buffers[0], *posext)
      for buff in self._back_buffers[1:-1]:
        pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, *BOARD_SIZE)
        pixbuf.get_from_drawable(buff, self._colormap, *posext)
        pixbuf = pixbuf.add_alpha(True, '\xFF', '\xFF', '\xFF')
        self._area.draw_pixbuf(self._gc, pixbuf, *posext)

class ImageLoader(object):
  
  @staticmethod
  def _load_sprite(name):
    from source.errors import Logger
    logger = Logger.instance()
    
    try:
      if name.split("_")[0] == "kyewarper":
        xpm = xpmdata.kyewarper
      elif name.split("_")[0] == "objwarper":
        xpm = xpmdata.objwarper
      elif name == "sign":
        xpm = xpmdata.note
      else:
        xpm = getattr(xpmdata, name)
      return gtk.gdk.pixbuf_new_from_xpm_data(xpm)
    except AttributeError, e:
      logger.log(e)
  
  @classmethod
  def load(cls):
    from source.errors import Logger
    logger = Logger.instance()
    
    images = {}
    splash = None
    sign = None
    
    for id in tiles.tiles:
      data = tiles.tiles[id]["name"]
      images[id] = cls._load_sprite(data)
    sign = cls._load_sprite("sign")
    splash = cls._load_sprite("splash")
    return images, splash, sign
  

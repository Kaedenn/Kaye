#!/usr/bin/env python

"""
Kaye Core Logic Control

This module encapsulates the highest level of non-graphical information
processing.

The class 'CoreControl' provides an interface to the graphics driver with a set
of callbacks. The CoreControl class is interested in the following set of
events:
  -- player decides to load a level
  -- player unloads a level (completes it, dies, etc)
  -- timer, every 0.25 seconds
  -- player presses one of the following keys:
      Up, Left, Down, Right
"""

import copy
import sys

from source import animator
from source import errors
from source import events
from source import schema
from source import tiles
from source import types

class Logic(object):
  
  MAX_LIVES = 3
  
  def __init__(self):
    self._scheme = None
    self._level = None
    self._lives = Logic.MAX_LIVES
    self._diamonds = [0, 0]
    self._animator = animator.Animator()
  
  def _inputmethod(self, func, *args, **kwargs):
    if not self.loaded:
      return
    try:
      result = func(*args, **kwargs)
    except events.KyeKilledEvent, event:
      # render lives
      self._ui.render(False, True, False, False, False)
      self._handle_die()
    else:
      if result:
        if result & self._animator.RES_FOUND_DIAMOND:
          self._diamonds[0] = self._diamonds[0] + 1
          # render diamonds
          self._ui.render(False, False, True, False, False)
          if self._check_win():
            self._handle_win()
        if result & self._animator.RES_FOUND_SIGN:
          row, col = tiles.logic.find_kye(self._level["tiles"])[:-1]
          sign = self._level["signs"][(row, col)]
          # render signs
          self._ui.render(False, False, False, False, True)
          self._ui.display_sign(sign["sign"])
          if sign["once"]:
            del self._level["signs"][(row, col)]
            self._animator.inform(self._level["signs"])
  
  def _start_scheme(self):
    self._lives = Logic.MAX_LIVES
    self._start_level()
  
  def _start_level(self):
    self._level = schema.grab_level(self._scheme)
    self._animator.inform(self._level["signs"])
    self._diamonds = [0, schema.count_diamonds(self._level)]
    self._ui.render()
    self._ui.dialog_box(self._ui.DB_BEGIN, self._level["hint"])
  
  def _check_win(self):
    return self.loaded and self._diamonds[0] == self._diamonds[1]
  
  def _handle_win(self):
    self._ui.render()
    self._ui.dialog_box(self._ui.DB_COMPLETE, self._level["msg_win"])
    del self._scheme["levels"][0]
    if self._scheme["levels"]:
      self._start_level()
    else:
      self._ui.dialog_box(self._ui.DB_COMPLETE, self._scheme["msg_win"])
      self.unload_scheme()
  
  def _handle_die(self):
    self._lives = self._lives - 1
    if self._lives == 0:
      self._ui.dialog_box(self._ui.DB_FAIL, self._scheme["msg_lose"])
      self.unload_scheme()
    else:
      if self._ui.dialog_box(self._ui.DB_DIE, self._level["msg_lose"]):
        self._start_level()
      else:
        self.unload_scheme()
  
  def sync_ui_engine(self, ui):
    self._ui = ui
  
  @property
  def loaded(self):
    return self._level is not None
  
  def load_scheme(self, filename):
    try:
      self._scheme = schema.load(filename)
    except errors.KayeError, e:
      self._scheme = None
      sys.stderr.write(str(e) + "\n")
      sys.stderr.write("loading scheme %s aborted\n" % filename)
      raise   # to pass it along to the gui class, since it expects it too
    else:
      self._animator = animator.Animator()
      self._start_scheme()
  
  def unload_scheme(self):
    self._scheme = None
    self._level = None
    self._lives = Logic.MAX_LIVES
    self._diamonds = [0, 0]
    self._ui.render()
  
  def get_drawing_info(self):
    return (self._level["tiles"], self._lives, self._diamonds,
            self._level["hint"], self._level["signs"])
  
  def cb_timer(self):
    self._inputmethod(self._animator.anim_timer, self._level["tiles"])
  
  def cb_key_up(self):
    self._inputmethod(self._animator.anim_up, self._level["tiles"])
  
  def cb_key_left(self):
    self._inputmethod(self._animator.anim_left, self._level["tiles"])
  
  def cb_key_down(self):
    self._inputmethod(self._animator.anim_down, self._level["tiles"])
  
  def cb_key_right(self):
    self._inputmethod(self._animator.anim_right, self._level["tiles"])
  
  

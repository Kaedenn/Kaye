#!/usr/bin/env python

"""
Kaye Bridge Class

This class will bridge the gap of responsibilities between the Glade and Logic
classes.
"""

from source import errors
from source import gui
from source import logic

class Kaye(object):
  """
  Kaye Bridge Class
  
  See the module's docstring for more information.
  """
  def __init__(self):
    errors.Logger.instance("errors.log")
    
    self._gui = gui.Glade()
    self._logic = logic.Logic()
    
    self._gui.sync_logic_engine(self._logic)
    self._logic.sync_ui_engine(self._gui)
  
  def main(self):
    self._gui.main()


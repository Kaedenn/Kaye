#!/usr/bin/env python

"""
Kaye Core Graphics Control: Gtk+ Implementation
"""

import functools
import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject # for timeout

from source import errors
from source import path
from source import resources
from source import tiles

import cProfile

# thanks to habnabit from ##python on Freenode for this little thing
def _inputmethod(func): 
  @functools.wraps(func)
  def wrapper(self, *a, **kw): 
    if not self._active:
      return
    elif not self._core_control or not self._core_control.loaded:
      return
    return func(self, *a, **kw)
  return wrapper

def _callbackmethod(func):
  @functools.wraps(func)
  def wrapper(self, *a, **kw):
    try:
      return func(self, *a, **kw)
    except errors.KayeError, e:
      from traceback import format_exc
      self._logger.log(format_exc(e))
      title = "Kaye Error"
      message = str(e)
      self._display_error(title, message)
    except RuntimeError, e:
      from traceback import format_exc
      self._logger.log("Critical Internal Error:")
      self._logger.log(format_exc(e))
      title = "Critical Internal Kaye Error"
      message = str(e)
      self._display_error(title, message)
      title = "Abnormal Program Termination"
      message = "Output saved in file %s; quitting gracefully"
      self._display_error(title, message)
      self._quit()
  return wrapper

class Glade(object):
  
  DB_BEGIN = 1
  DB_COMPLETE = 1 << 1 | DB_BEGIN
  DB_DIE = 1 << 2 | DB_COMPLETE
  DB_FAIL = 1 << 3 | DB_DIE
  
  RIDs = {
    "ok" : 1,
    "cancel" : 2,
    "close" : 3
  }
  
  def __init__(self):
    self._glade = {
      "main" : path.srcpath("glade/main.glade"),
      "open" : path.srcpath("glade/open.glade"),
      "about" : path.srcpath("glade/about.glade"),
    }
    
    self._core_control = None
    
    self._logger = errors.Logger.instance()
    
    self._main_callbacks = {
      "main_destroy" : self._quit,
      "file_open_handler" : self._file_open,
      "file_quit_handler" : self._quit,
      "help_about_handler" : self._help_about,
      "expose_handler" : self._redraw,
      "focus_in_handler" : self._focus_in,
      "focus_out_handler" : self._focus_out,
      "key_press_handler" : self._key_press
    }
    
    self._glade_main = gtk.glade.XML(self._glade["main"])
    self._glade_main.signal_autoconnect(self._main_callbacks)
    
    self._window = self._glade_main.get_widget("MainWindow")
    self._window.set_icon_from_file(path.srcpath("resources/pie.ico"))
    self._window.show()
    
    area = self._glade_main.get_widget("GameField")
    area.show()
    
    images = resources.ImageLoader.load()
    self._drawer = resources.Drawer(area.window, *images)
    
    self._active = False
    self._activate()
    
    self._drawer.render_splash()
  
  def sync_logic_engine(self, logic):
    if not self._core_control:
      self._core_control = logic
    
    self._keybindings = {
      gtk.keysyms.Up : self._core_control.cb_key_up,
      gtk.keysyms.Left : self._core_control.cb_key_left,
      gtk.keysyms.Down : self._core_control.cb_key_down,
      gtk.keysyms.Right : self._core_control.cb_key_right
    }
    
    self._callbacks = {
      "timer" : self._core_control.cb_timer,
      "load" : self._core_control.load_scheme,
      "unload" : self._core_control.unload_scheme
    }
    
    self.render()
  
  def _display_error(self, title, message):
    dialog = gtk.MessageDialog(self._window, gtk.DIALOG_MODAL,
                               gtk.MESSAGE_ERROR, gtk.BUTTONS_OK)
    dialog.set_title(title)
    dialog.format_secondary_text(message)
    dialog.show()
    dialog.run()
    dialog.destroy()
  
  @_callbackmethod
  def dialog_box(self, dbtype, message):
    """
    Supported types:
      begin {name, hint} -> None
      complete {name, success} -> None
      die {name, die} -> bool (retry, quit)
      fail {name, fail} -> None
    """
    flag, type = gtk.DIALOG_MODAL, gtk.MESSAGE_INFO
    dbs = {
      self.DB_BEGIN : (
        (gtk.BUTTONS_OK, "Ready?"),
        lambda reponse: None
      ),
      self.DB_COMPLETE : (
        (gtk.BUTTONS_OK, "Congratulations!"),
        lambda reponse: None
      ),
      self.DB_DIE : (
        (gtk.BUTTONS_YES_NO, "Try Again?"),
        lambda reponse: res == gtk.RESPONSE_YES
      ),
      self.DB_FAIL : (
        (gtk.BUTTONS_OK, "Game Over"),
        lambda reponse: None
      )
    }
    if not dbtype in dbs:
      raise RuntimeError("gui.glade.cb_dialog_box(): unknown dialog type: %s"
        % dbtype)
    
    dialog = gtk.MessageDialog(self._window, flag, type, *dbs[dbtype][0])
    dialog.set_title(dbs[dbtype][0][-1])
    dialog.format_secondary_text(message)
    dialog.show()
    result = dialog.run()
    dialog.destroy()
    
    return dbs[dbtype][1](result)
  
  def display_sign(self, text):
    dialog = gtk.MessageDialog(self._window, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK, "A message from Kaye...")
    dialog.set_title("Sign")
    dialog.format_secondary_text(text)
    dialog.show()
    dialog.run()
    dialog.destroy()
  
  def render(self, tiles = True, lives = True, diamonds = True, hint = True,
             signs = True):
    if self._core_control is None or not self._core_control.loaded:
      bar = self._glade_main.get_widget("LivesLeftBar")
      bar.set_fraction(0.0)
      bar.set_text("")
      bar = self._glade_main.get_widget("DiamondsLeftBar")
      bar.set_fraction(0.0)
      bar.set_text("")
      bar = self._glade_main.get_widget("HintBar")
      bar.set_text("Welcome to Kaye!")
    else:
      drawing_info = self._core_control.get_drawing_info()
      if tiles:
        self._drawer.render_tiles(drawing_info[0])
      if lives:
        bar = self._glade_main.get_widget("LivesLeftBar")
        maxlives = self._core_control.MAX_LIVES
        bar.set_fraction(min(drawing_info[1] * 1.0 / maxlives, 1.0))
        if drawing_info[1] == 1:
          bar.set_text("1 Life")
        else:
          bar.set_text("%s Lives" % (drawing_info[1],))
      if diamonds:
        bar = self._glade_main.get_widget("DiamondsLeftBar")
        bar.set_fraction(drawing_info[2][0] * 1.0 / drawing_info[2][1])
        bar.set_text("%s of %s" % tuple(drawing_info[2]))
      if hint:
        bar = self._glade_main.get_widget("HintBar")
        bar.set_text(drawing_info[3])
      if signs:
        self._drawer.render_signs(drawing_info[4])
  
  def _activate(self):
    if not self._active:
      self._active = True
      if self._core_control and self._core_control.loaded:
        self._timer = gobject.timeout_add(250, self._timer_tick)
      else:
        self._timer = None
  
  def _deactivate(self):
    if self._active:
      self._active = False
      if self._timer:
        gobject.source_remove(self._timer)
  
  @_callbackmethod
  def _file_open(self, widget, data = None):
    fsel = gtk.glade.XML(self._glade["open"]).get_widget("OpenDialog")
    filt = gtk.FileFilter()
    filt.add_pattern("*.nks")
    fsel.set_filter(filt)
    fsel.set_filename(path.rootpath("schema/default.nks"))
    fsel.set_icon_from_file(path.srcpath("resources/pie.ico"))
    fsel.show()
    response = fsel.run()
    filename = fsel.get_filename()
    #fsel.get_filter().destroy()
    fsel.destroy()
    if response == Glade.RIDs["ok"]:
      try:
        self._callbacks["load"](filename)
      except errors.KayeError, e:
        self._display_error("Error in loading", str(e))
      else:
        self.render()
  
  @_callbackmethod
  def _quit(self, widget, data = None):
    self._window.destroy()
    gtk.main_quit()
  
  @_callbackmethod
  def _help_about(self, widget, data = None):
    dialog = gtk.glade.XML(self._glade["about"]).get_widget("AboutDialog")
    dialog.show()
    dialog.run()
    dialog.destroy()
  
  @_callbackmethod
  def _redraw(self, area, event):
    if self._core_control is None or not self._core_control.loaded:
      self._drawer.render_to_area(True)
    else:
      self._drawer.render_to_area()
  
  @_callbackmethod
  def _focus_in(self, widget, data = None):
    self._activate()
  
  @_callbackmethod
  def _focus_out(self, widget, data = None):
    self._deactivate()
  
  @_callbackmethod
  @_inputmethod
  def _key_press(self, widget, data = None):
    if data.keyval in self._keybindings:
      self._keybindings[data.keyval]()
      self.render(True, False, False, False, False)
  
  @_callbackmethod
  @_inputmethod
  def _timer_tick(self):
    self._callbacks["timer"]()
    self.render(True, False, False, False, False)
    self._timer = gobject.timeout_add(250, self._timer_tick)
  
  def main(self):
    if not self._core_control:
      raise RuntimeError("gui.Glade.main(): logic engine not loaded")
    else:
      gtk.main()
  


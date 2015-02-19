#!/usr/bin/env python

"""
Error Tree:

KayeError (error)
  LogicError (error)
  FileError (filename, error)
    XMLError (filename, error)
  LevelError (name, error)
    MissingKyeError (name)
    DiamondError (name)
    TilePointError (name, row, col, error)
      InvalidTileError (name, id, row, col)
      TupleError (name, id, row, col, degree)
      MultipleKyeError (name, row, col)
      WallError (name, row, col)
"""

from path import rootpath

from traceback import format_exc

class Logger(object):
  _instance = None
  
  @classmethod
  def instance(cls, *args):
    if not cls._instance:
      cls._instance = cls(*args)
    return cls._instance
  
  def __init__(self, filename = "errors.log"):
    if not self._instance:
      self._instance = self
    self._filename = filename
    self._file = rootpath(filename)
  
  def getfilename(self):
    return self._filename
  
  def log(self, exception):
    file = open(self._file, "wa")
    file.write(format_exc(exception) + "\n")
    file.close()

class KayeError(RuntimeError):
  def __init__(self, error):
    super(KayeError, self).__init__(error.replace(":", ":\n"))

class LogicError(KayeError):
  def __init__(self, error):
    super(LogicError, self).__init__(error)

class FileError(KayeError):
  def __init__(self, filename, error):
    super(FileError, self).__init__("Error in '%s': %s" % (filename, error))

class XMLError(FileError):
  def __init__(self, filename, error):
    super(XMLError, self).__init__(filename, "XML tag error: %s" % error)

class LevelError(KayeError):
  def __init__(self, name, error):
    s = "Error in level '%s': %s"
    super(LevelError, self).__init__(s % (name, error))

class MissingKyeError(LevelError):
  def __init__(self, name):
    s = "did not find a 'Kye' tile"
    super(MissingKyeError, self).__init__(name, s)

class DiamondError(LevelError):
  def __init__(self, name):
    s = "did not find a single diamond"
    super(DiamondError, self).__init__(name, s)

class TilePointError(LevelError):
  def __init__(self, name, row, col, error):
    s = "Tile error at row %s, col %s: %s"
    super(TilePointError, self).__init__(name, s % (row, col, error))

class InvalidTileError(TilePointError):
  def __init__(self, name, id, row, col):
    s = "unknown tile ID '%.2x'"
    super(InvalidTileError, self).__init__(name, row, col, s % (id,))

class TupleError(TilePointError):
  def __init__(self, name, id, row, col, degree):
    s = "tile '%.2x' required exactly zero or %s time(s)"
    super(TupleError, self).__init__(name, row, col, s % (id, degree))

class MultipleKyeError(TilePointError):
  def __init__(self, name, row, col):
    s = "found tile 'Kye' more than once"
    super(MultipleKyeError, self).__init__(name, row, col, s)

class WallError(TilePointError):
  def __init__(self, name, row, col):
    s = "entire level must be enclosed by square walls"
    super(WallError, self).__init__(name, row, col, s)


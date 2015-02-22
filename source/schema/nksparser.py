#!/usr/bin/env python

import os
import xml
import xml.dom.minidom

from source import errors
from source.tiles import logic
from source import types
from source.schema import nksvalidator

class Parser(object):
  def __init__(self, filename = ""):
    self._filename = ""
    self._lines = []
    self._scheme = {}
    if filename:
      self.set_file(filename)

  def _get_text(self, node):
    text = ""
    for n in node.childNodes:
      if n.nodeType in (n.TEXT_NODE, n.CDATA_SECTION_NODE):
        text = text + n.data
    return text

  def _get_text_elem(self, node, child):
    return self._get_text(node.getElementsByTagName(child)[0])

  def _get_attr(self, node, attr):
    try:
      return node.attributes[attr].value
    except KeyError, e:
      xml_str = node.toprettyxml()
      error = "did not find attribute '%s' of node '%s'" % (attr, xml_str)
      raise errors.XMLError(self._filename, error)

  def _generate_scheme_tree(self):
    """
    Generates a scheme from self._lines, as supplied by either __init__ or
    self.set_file
    """
    scheme = {}
    tree = xml.dom.minidom.parseString(self._lines)
    root = tree.documentElement
    scheme["name"] = self._get_attr(root, "name")
    scheme["description"] = self._get_text_elem(root, "description")
    scheme["msg_win"] = self._get_text_elem(root, "complete")
    scheme["msg_lose"] = self._get_text_elem(root, "lose")
    scheme["levels"] = list()
    # for each level...
    for node in root.getElementsByTagName("level"):
      level = dict()
      # set the messages
      level["name"] = self._get_attr(node, "name")
      level["hint"] = self._get_text_elem(node, "hint")
      level["msg_win"] = self._get_text_elem(node, "complete")
      level["msg_lose"] = self._get_text_elem(node, "lose")
      # load the tiles and tally them for later
      board = types.Board()
      rawtiles = self._get_text_elem(node, "tiles")
      for row, rowtiles in enumerate(rawtiles.strip().split('\n')):
        for col, t in enumerate(rowtiles.strip().split()):
          t = int(t, 16)
          logic.push_tile(board[row][col], types.Tile(t))
          # board[row][col][tiles.tiles[t]["layer"]] = types.Tile(t)
      level["tiles"] = board
      # load the signs
      level["signs"] = dict()
      for event in node.getElementsByTagName("sign"):
        newsign = dict()
        pos = int(self._get_attr(event, "row")), int(self._get_attr(event, "col"))
        once = {"true" : True}.get(self._get_attr(event, "once"), False)
        newsign["once"] = once
        newsign["sign"] = self._get_text(event).strip()
        level["signs"][pos] = newsign
      scheme["levels"].append(level)

    tree.unlink()
    self._scheme = scheme

  def set_file(self, filename):
    self._filename = filename
    try:
      file = open(filename, "r")
      self._lines = file.read()
      file.close()
    except IOError, e:
      raise errors.FileError(filename, os.strerror(e.errno))

  def get_scheme(self):
    if not self._lines or not self._filename:
      this = "source.schema.nksparser.Parser.get_scheme()"
      error_str = "in " + this + ": filename has not been specified"
      raise errors.KayeError(error_str)
    try:
      self._generate_scheme_tree()
      nksvalidator.validate_scheme(self._filename, self._scheme)
    except xml.parsers.expat.ExpatError, e:
      raise errors.XMLError(self._filename, e)
    else:
      return self._scheme


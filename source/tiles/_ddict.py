#!/usr/bin/env python

"""
Double-dict: a dictionary type where both the keys and values act like keys.

Example:
  d = ddict({"key1" : "value1", "key2" : "value2"})
  print d["key1"] # prints "value1"
  print d["value2"] # prints "key2"
"""

class ddict(dict):
  
  def __init__(self, d = None, **kwargs):
    items = {}
    if d is not None:
      for i in d:
        items[i] = d[i]
        items[d[i]] = i
    for i in kwargs:
      items[i] = kwargs[i]
      items[kwargs[i]] = i
    super(ddict, self).__init__(self, **items)
  
  def __getitem__(self, name):
    return super(ddict, self).__getitem__(name)
  
  def __setitem__(self, name, value):
    if name in self: del self[name]
    if value in self: del self[value]
    super(ddict, self).__setitem__(name, value)
    super(ddict, self).__setitem__(value, name)
  
  def __delitem__(self, name):
    super(ddict, self).__delitem__(self[name])
    super(ddict, self).__delitem__(name)
  
  def __repr__(self):
    unique = {}
    for k in self:
      if not self[k] in unique:
        unique[k] = self[k]
    return "ddict(" + repr(unique) + ")"
  
  def __len__(self):
    return super(ddict, self).__len__() / 2
  


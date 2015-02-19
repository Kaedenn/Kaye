#!/usr/bin/env python

import os.path

path = os.path.dirname(os.path.abspath(__file__))
rtpath = os.path.abspath(os.path.join(path, os.path.pardir))

def srcpath(*paths):
  return os.path.abspath(os.path.join(rtpath, "source", *paths))

def rootpath(*paths):
  return os.path.abspath(os.path.join(rtpath, *paths))


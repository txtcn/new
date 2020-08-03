#!/usr/bin/env python


class Find:
  def __init__(self):
    pass


if __name__ == "__main__":
  from glob import glob
  find = Find()
  for i in glob("/share/txt/data/*.zd"):
    find << i

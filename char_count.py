#!/usr/bin/env python

import zd
from os.path import join, dirname, abspath
from json import dump
from collections import Counter

ARROW = "➜"
_DIR = dirname(abspath(__file__))


class Parse:
  def __init__(self):
    self.count = Counter()
    self.total = 0

  def __call__(self, title, txt):
    self.total += 1
    count = self.count
    for line in txt[1:]:
      for i in line:
        if i not in ", \r\n":
          count[i] += 1
    if self.total % 1000 == 0:
      print(self.total)
      self.dump()

  def dump(self):
    r = {}
    for k, v in self.count.items():
      if v > 1000:
        r[k] = v
    with open(join(_DIR, "char.json"), "w") as f:
      dump(r, f, ensure_ascii=False)


def main():
  from os import walk
  from tqdm import tqdm
  parse = Parse()
  fileli = []

  for root, _, file_li in walk("/share/txt/data"):
    for filename in file_li:
      if filename.endswith(".zd"):
        filepath = join(root, filename)
        fileli.append(filepath)

  for filepath in tqdm(fileli):
    with zd.open(filepath) as f:
      it = iter(f)
      title = None
      txt = []
      for i in it:
        i = i.lower()
        if i.startswith(ARROW):
          if title:
            parse(title, txt)
          title = i[1:]
          txt = []
        else:
          txt.append(i)
      if title:
        parse(title, txt)
  parse.dump()


main()

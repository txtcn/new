#!/usr/bin/env python

from _title_word import ngram_line, ngram, run
from collections import Counter, defaultdict
from os.path import abspath, dirname, join
from cn import tokenize

_DIR = dirname(abspath(__file__))


class Parse:
  def __init__(self):
    count = {}
    with open(join(_DIR, "title_word.txt")) as f:
      it = iter(f)
      self.total = int(next(it)[:-1])
      for i in f:
        word, n = i.rstrip("\n").rsplit(",", 1)
        word = tuple(tokenize(word))
        count[word] = int(n)
    self.count = count

  def __call__(self, title, txt):
    count = self.count
    r = set()
    for i in ngram_line(txt):
      if i in count:
        r.add(i)
    return r


run(__file__, Parse())

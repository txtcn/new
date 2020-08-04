#!/usr/bin/env python

from _title_word import ngram_line, run, total_count


class Parse:
  def __init__(self):
    self.total, self.count = total_count("title_word")

  def __call__(self, title, txt):
    count = self.count
    r = set()
    for i in ngram_line(txt):
      if i in count:
        r.add(i)
    return r


run(__file__, Parse())

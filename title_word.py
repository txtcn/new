#!/usr/bin/env python

from _title_word import ngram_line, ngram, run
from collections import Counter, defaultdict


def parse_word(title, txt):
  count = defaultdict(int)

  # word_set = set()
  total = len(title) + len(txt)

  for i in ngram_line(title):
    if len(i) > 1:
      count[i] = 1

  for i in ngram_line(txt):
    if i in count:
      count[i] += 1

  for word, n in sorted(count.items(), key=lambda x: len(x[0])):
    if n >= 3:
      if len(word) > 2:
        for i in ngram(word, len(word)):
          count[i] -= n

  r = []
  for word, n in count.items():
    len_word = len(word)
    if len_word > 2:
      for i in ngram(word, len_word):
        if n < count[i]:
          n = 0
          break

    if n > 3 and (n * len(word)) / total > 0.005:
      r.append(word)
  return r


run(__file__, parse_word)

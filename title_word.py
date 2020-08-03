#!/usr/bin/env python
import zd
from cn import tokenize, RE_PUNCTUATION
from nltk import ngrams
from collections import Counter
from operator import itemgetter


def ngram(li, size):
  for n in range(2, size):
    for i in ngrams(li, n):
      yield i


def ngram_line(txt):
  for s in RE_PUNCTUATION.split(txt):
    li = tokenize(s)
    for i in ngram(li, 8):
      yield i


def find_word(title, txt):
  count = Counter()

  for i in ngram_line(title):
    if len(i) > 1:
      count[i] += 1

  total = len(title) + sum(len(i) for i in txt)
  for line in txt:
    for i in ngram_line(line):
      if i in count:
        count[i] += 1

  for word, n in count.items():
    if n > 3:
      if len(word) > 2:
        for i in ngram(word, len(word)):
          count[i] -= n

  r = []
  for word, n in count.items():
    if n > 3 and (n * len(word)) / total > 0.005:
      _word = "".join(word)
      r.append(_word)
  return r


class Find:
  def __init__(self):
    self.count = Counter()
    self.total = 0

  def _word(self, title, txt):
    for i in find_word(title, txt):
      self.count[i] += 1

  def __lshift__(self, filepath):
    self.total += 1
    with zd.open(filepath) as f:
      txt = []
      title = None
      it = iter(f)
      for i in it:
        i = i[:-1].lower()
        if i.startswith("➜"):
          next(it)
          if title:
            self._word(title, txt)
          title = i[1:]
          txt = []
        else:
          if i:
            txt.append(i)
      if title:
        self._word(title, txt)


if __name__ == "__main__":
  from os import walk
  from os.path import join

  find = Find()
  for root, _, file_li in walk("/share/txt/data"):
    for filename in file_li:
      if filename.endswith(".zd"):
        filepath = join(root, filename)
        print(filepath)
        find << filepath
        min_n = max(int(find.total * 0.0001), 3)
        for k, v in sorted(find.count.items(), key=itemgetter(1)):
          if v > min_n:
            print(k, v)

      # input()

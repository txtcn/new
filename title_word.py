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
    for i in ngram(li, 12):
      yield i


def parse_word(title, txt):
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


def _parse(filepath):
  count = Counter()

  def _word(title, txt):
    for i in parse_word(title, txt):
      count[i] += 1

  total = 0

  with zd.open(filepath) as f:
    txt = []
    title = None
    it = iter(f)
    for i in it:
      i = i[:-1].lower()
      if i.startswith("➜"):
        next(it)
        if title:
          _word(title, txt)
        title = i[1:]
        txt = []
        total += 1
      else:
        if i:
          txt.append(i)
    if title:
      _word(title, txt)

  return total, dict(count)


class Parse:
  def __init__(self):
    self.count = Counter()
    self.total = 0

  def __call__(self, total, count):
    self.total += total
    self.count += Counter(count)


if __name__ == "__main__":
  from os import walk, cpu_count
  from os.path import join, dirname, basename, abspath
  from concurrent.futures import ProcessPoolExecutor, as_completed

  outfile = abspath(__file__)[:-2] + "txt"
  parse = Parse()
  with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
    todo = {}
    for root, _, file_li in walk("/share/txt/data"):
      for filename in file_li:
        if filename.endswith(".zd"):
          filepath = join(root, filename)
          todo[executor.submit(_parse, filepath)] = filepath
    for future in as_completed(todo):
      filepath = todo[future]
      print(filepath)
      try:
        r = future.result()
      except Exception as exc:
        print(exc)
      else:
        parse(*r)
        min_n = max(int(parse.total * 0.00001), 3)
        with open(outfile, "w") as out:
          out.write(str(parse.total) + "\n")
          for k, v in sorted(parse.count.items(), key=itemgetter(1), reverse=True):
            if v > min_n:
              out.write("%s,%s\n" % (k, v))

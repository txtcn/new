#!/usr/bin/env python
import zd
from cn import tokenize, RE_PUNCTUATION
from nltk import ngrams
from collections import Counter, defaultdict
from operator import itemgetter
from acora import AcoraBuilder
from itertools import groupby

utf8 = 'utf8'


def ngram(li, size):
  for n in range(2, size):
    for i in ngrams(li, n):
      yield i


def ngram_line(txt):
  for s in RE_PUNCTUATION.split(txt):
    li = tokenize(s)
    for i in ngram(li, min(14, 1 + len(li))):
      yield i


def parse_word(title, txt):
  count = Counter()

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


ARROW = "➜"


def _parse(filepath):
  count = Counter()

  def _word(title, txt):
    for i in parse_word(title, "\n".join(txt[1:])):
      count[i] += 1

  total = 0

  with zd.open(filepath) as f:
    it = iter(f)
    title = None
    txt = []
    for i in it:
      i = i.lower()
      if i.startswith(ARROW):
        if title:
          _word(title, txt)
        title = i[1:]
        txt = []
        total += 1
      else:
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


def word_join(li):
  r = []
  pre_ascii = False
  for i in range(len(li)):
    t = li[i]
    is_ascii = t.isascii()
    if pre_ascii and is_ascii:
      t = " " + t
    r.append(t)
    pre_ascii = is_ascii
  return "".join(r)


if __name__ == "__main__":
  from os import walk, cpu_count
  from os.path import join, dirname, basename, abspath
  # from concurrent.futures import ThreadPoolExecutor as ProcessPoolExecutor, as_completed
  from concurrent.futures import ProcessPoolExecutor, as_completed
  from tqdm import tqdm

  outfile = abspath(__file__)[:-2] + "txt"
  print(outfile)
  parse = Parse()
  with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
    todo = {}
    for root, _, file_li in walk("/share/txt/data"):
      for filename in file_li:
        if filename.endswith(".zd"):
          filepath = join(root, filename)
          # _parse(filepath)
          todo[executor.submit(_parse, filepath)] = filepath
    pbar = tqdm(total=len(todo))
    for future in as_completed(todo):
      pbar.update(1)
      filepath = todo[future]
      print(">", filepath)
      try:
        r = future.result()
      except Exception as exc:
        print("Exception", exc)
      else:
        parse(*r)
        min_n = max(int(parse.total * 0.000001), 3)
        t = [str(parse.total)]
        for k, v in sorted(parse.count.items(), key=itemgetter(1), reverse=True):
          if v > min_n:
            t.append("%s,%s" % (word_join(k), v))
        t = "\n".join(t)
        with open(outfile, "w") as out:
          out.write(t)
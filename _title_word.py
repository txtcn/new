#!/usr/bin/env python
import zd
from cn import tokenize, RE_PUNCTUATION
from nltk import ngrams
from collections import Counter, defaultdict
from operator import itemgetter
from os.path import join, dirname, abspath

utf8 = 'utf8'

_DIR = dirname(abspath(__file__))


def total_count(filename):
  count = {}
  with open(join(_DIR, filename + ".txt")) as f:
    it = iter(f)
    total = int(next(it)[:-1])
    for i in f:
      word, n = i.rstrip("\n").rsplit(",", 1)
      word = tuple(tokenize(word))
      count[word] = int(n)
  return total, count


def ngram(li, size):
  for n in range(2, size):
    for i in ngrams(li, n):
      yield i


def ngram_line(txt):
  for line in txt.split("\n"):
    if line:
      for s in RE_PUNCTUATION.split(line):
        li = tokenize(s)
        for i in ngram(li, min(14, 1 + len(li))):
          yield i


ARROW = "➜"


def _parse(parse_word, filepath):
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


def run(outfile, parse_word):
  from os import walk, cpu_count
  # from concurrent.futures import ThreadPoolExecutor as ProcessPoolExecutor, as_completed
  from concurrent.futures import ProcessPoolExecutor, as_completed
  from tqdm import tqdm

  outfile = abspath(outfile)[:-2] + "txt"
  print(outfile)
  parse = Parse()
  with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
    todo = {}
    for root, _, file_li in walk("/share/txt/cn"):
      for filename in file_li:
        if filename.endswith(".zstd"):
          filepath = join(root, filename)
          # _parse(filepath)
          todo[executor.submit(_parse,
                               parse_word,
                               filepath)] = filepath
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

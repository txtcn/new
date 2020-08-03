#!/usr/bin/env python
import zd
from cn import tokenize
import re
from nltk import ngrams
from collections import Counter

RE_PUNCTUATION = re.compile(
  r"""[\[\]\(\)\?\!;'"。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰—‘’‛“”„‟…﹏]+"""
)


def ngram(txt):
  for s in RE_PUNCTUATION.split(txt):
    li = tokenize(s)
    for n in range(2, 8):
      for i in ngrams(li, n):
        yield i


def find_word(title, txt):
  count = Counter()

  for i in ngram(title):
    count[i] += 1

  for line in txt:
    for i in ngram(line):
      if i in count:
        count[i] += 1

  for word, n in sorted(count.items(), key=lambda x: x[1]):
    print(word, n)

  input()


class Find:
  def __init__(self):
    pass

  def __lshift__(self, filepath):

    with zd.open(filepath) as f:
      txt = []
      title = None
      it = iter(f)
      for i in it:
        i = i[:-1].lower()
        if i.startswith("➜"):
          next(it)
          if title:
            find_word(title, txt)
          title = i[1:]
          txt = []
        else:
          if i:
            txt.append(i)
      if title:
        find_word(title, txt)


if __name__ == "__main__":
  from os import walk
  from os.path import join

  find = Find()
  for root, _, file_li in walk("/share/txt/data"):
    for filename in file_li:
      if filename.endswith(".zd"):
        filepath = join(root, filename)
        find << filepath

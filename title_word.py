#!/usr/bin/env python
import zd
from cn import tokenize
import re
from nltk import ngrams
from collections import Counter

RE_PUNCTUATION = re.compile(
  r"""[\[\]\(\)\?\!;'"。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰—‘’‛“”„‟…﹏]+"""
)


def find_word(title, txt):
  title = title.lower()
  count = Counter()

  for s in RE_PUNCTUATION.split(title):
    li = tokenize(s)
    for n in range(2, 8):
      for i in ngrams(li, n):
        count[i] += 1

  for line in txt:
    for i in RE_PUNCTUATION.split(line):
      print(i)

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
        i = i[:-1]
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
  from glob import glob
  find = Find()
  for i in glob("/share/txt/data/*.zd"):
    find << i

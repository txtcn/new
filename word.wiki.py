#!/usr/bin/env python

import zd
from fire import Fire


@Fire
def main(
  title_zd_path="/share/txt/wiki/zhwiki-20200701-pages-articles.title.txt.zd"
):
  word_set = set()
  with zd.open(title_zd_path) as f:
    for i in f:
      i = i[:-1].replace('（', '(').split("(", 1)[0]
      len_i = len(i)
      if len_i <= 1 or len_i > 7 or i.isascii():
        continue
      if i[0].isdigit() and '年' in i:
        continue
      word_set.add(i.lower())

  for i in sorted(word_set):
    print(i)

#!/usr/bin/env python

from _title_word import total_count, word_join
from operator import itemgetter


def main():
  total_title, count_title = total_count("title_word")
  total_txt, count_txt = total_count("title_word.2")
  total_txt += 1
  r = []
  for k, v in count_title.items():
    p = (v * total_txt) / ((count_txt.get(k, 0) + 1) * total_title)
    r.append((word_join(k), int(p * 1000000)))
  for i in sorted(r, key=itemgetter(1), reverse=True):
    print("%s,%s" % i)


if __name__ == "__main__":
  main()

#!/usr/bin/env python
from os.path import join
from os import walk
import zd
from io import StringIO
from LAC import LAC


def site_iter(dirpath):
  for root, dirli, fileli in walk(dirpath):
    for filename in fileli:
      yield root, filename


def txt_iter(filepath):
  with zd.open(filepath) as f:
    f = iter(f)
    line = next(f)
    if not line:
      return
    r = [line[1:-1].lower()]
    next(f)
    for line in f:
      if line.startswith("➜"):
        yield r
        r = [line[1:-1].lower()]
        next(f)
      else:
        r.append(line[:-1].lower())
    yield r


def main():
  # 装载分词模型
  lac = LAC(mode='seg')

  dirpath = '/data/txtcn'
  for root, filename in site_iter(dirpath):
    filepath = join(root, filename)
    print(filename)
    for txt in txt_iter(filepath):
      for li in lac.run(txt):
        print(li)
      # input()


if __name__ == "__main__":
  main()

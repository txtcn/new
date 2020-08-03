#!/usr/bin/env python

import akshare as ak
from util.half import half
from os.path import dirname, abspath, basename
from tzutil.cout import cout
from time import sleep


def format_a(name):
  return half(name.replace(' ', '').lstrip("*")).lower()


class Name:
  def __init__(self):
    self.exist = set()

  def __str__(self):
    r = []
    for i in sorted(self.exist):
      r.append(i)
    return "\n".join(r)

  def __lshift__(self, name):
    name = name.strip().lower()
    if name and name not in self.exist:
      print(name)
      self.exist.add(name)


NAME = Name()


class StockA:
  def __init__(self):
    self.exist = set()

  def __call__(self, code, name):
    name = format_a(name)
    NAME << name
    if code not in self.exist:
      self.exist.add(code)
      cout.green << ("\n" + code, name)
      sleep(2)
      li = ak.stock_info_change_name(stock=code)
      for i in li:
        i = format_a(i)
        if i[0] in "g" or "(" in i or (
          i.startswith("s") and not i.startswith("st")
        ):
          continue
        NAME << i


def main():
  outfile = abspath(__file__)[:-2] + "txt"
  with open(outfile) as f:
    for i in f:
      i = i.strip("\n")
      if i:
        NAME << i
  stock_a = StockA()

  # A股全部
  li = ak.stock_info_a_code_name()
  for index, i in li.iterrows():
    stock_a(i['code'], i['name'])

  li = ak.stock_info_sz_delist(indicator="终止上市公司")
  for index, i in li.iterrows():
    stock_a(i['证券代码'], i['证券简称'])

  for func,attr in (
    (ak.stock_us_spot, 'cname'),
    (ak.stock_hk_spot,'name')
  ):
    li = func()
    for index, i in li.iterrows():
      name = i[attr].split("-")[0].replace("（", "(").split("(")[0]
      if name.isascii():
        continue
      if name.endswith("公司"):
        name = name[:-2]
      if name.endswith("类股") or ' ' in name or '&#' in name:
        continue
      NAME << name
  with open(outfile, "w") as out:
    out.write(str(NAME))


main()

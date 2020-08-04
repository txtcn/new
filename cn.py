import re

RE_PUNCTUATION = re.compile(
  r"""[\|\[\]\(\)\?\!;'"。！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰—‘’‛“”„‟…﹏]+"""
)


def tokenize(text):
  output = []
  t = []

  def append():
    nonlocal t
    if t:
      output.append(''.join(t))
      t = []

  for char in text:
    cp = ord(char)
    if _is_chinese_char(cp):
      append()
      output.append(char)
    else:
      char = char.strip()
      if not char:
        append()
      else:
        t.append(char)
  append()
  return output


def _is_chinese_char(cp):
  if ((cp >= 0x4E00 and cp <= 0x9FFF)
      or (cp >= 0x3400 and cp <= 0x4DBF)
      or (cp >= 0x20000 and cp <= 0x2A6DF)
      or (cp >= 0x2A700 and cp <= 0x2CEAF)
      or (cp >= 0xF900 and cp <= 0xFAFF)
      or (cp >= 0x2F800 and cp <= 0x2FA1F)):
    return True

  return False


# def has_chinese(s):
#   for i in s:
#     if i >= u'\u4e00' and i <= u'\u9fa5':
#       return True
#   return False
#
#
# def chinese_count(s):
#   count = 0
#   for i in s:
#     if i >= u'\u4e00' and i <= u'\u9fa5':
#       count += 1
#   return count
#
#
# def chinese_more_than(s, max_count):
#   count = 0
#   for i in s:
#     if i >= u'\u4e00' and i <= u'\u9fa5':
#       count += 1
#       if count > max_count:
#         return True
#
#
# def 全角转半角(ustring):
#   rstring = []
#   for uchar in ustring:
#     inside_code = ord(uchar)
#     if inside_code == 12288:  # 全角空格直接转换
#       inside_code = 32
#       uchar = 0
#     elif (
#       inside_code >= 65281 and inside_code <= 65374
#     ):  # 全角字符（除空格）根据关系转化
#       inside_code -= 65248
#       uchar = 0
#     rstring.append(uchar or chr(inside_code))
#   return "".join(rstring)
#
#
# def 去空格(s):
#   if s:
#     return s.strip("\n\r\xa0 \u00A0\u3000")
#
#
# def 短句窗口(s):
#   for line in s.replace("。", "\n").replace("?", "\n").replace(
#     "\r\n", "\n"
#   ).replace("\r", "\n").split("\n"):
#     for i in 按标点分割(line):
#       yield i
#
#
# 连字符 = ".-/&"
#
#
# def 按标点分割(s):
#   r = []
#   for i in s.replace("'", '"') + " ":
#     if (i >= u'\u4e00'
#         and i <= u'\u9fa5') or i.isalnum() or i in 连字符:
#       r.append(i)
#     else:
#       s = 去空格("".join(r))
#       if s and s not in 连字符:
#         yield s
#       r = []
#
#
# def 去标点(s):
#   return "".join(按标点分割(s))

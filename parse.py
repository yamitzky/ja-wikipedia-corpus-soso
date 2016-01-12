#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from HTMLParser import HTMLParser
import re
import sys

from lxml import etree


# 一部の{{template記法}}などを置換
SUB_TEMPLATES = [
    re.compile("{{仮リンク[|]([^|]+)[|][^{}]+}}"),  # {{仮リンク}}
    re.compile("{{lang[|][^|]+[|]([^|{}]+)}}", re.IGNORECASE),  # {{lang}}
    re.compile("{{lang-[^|\]]+[|]([^|{}]+)}}", re.IGNORECASE),  # {{lang-}}
    re.compile("{{en[|]([^|{}]+)}}", re.IGNORECASE),  # {{en}}
    re.compile("{{unicode[|]([^{}]+)}}", re.IGNORECASE),  # {{unicode}}
    re.compile("\[\[[^\]]+[|]([^|\]]+)\]\]"),  # [[記事リンク|]]
    re.compile("\[\[([^\] (]+) [(][^\])]+[)]\]\]"),  # [[記事リンク (括弧つき)]]
    re.compile("\[\[([^\]]+)\]\]"),  # [[記事リンク]]
    re.compile("'''*([^']+)'*''"),  # ''強調''
]
# 未知の{{template記法}}や引用タグは削除
DEL_TEMPLATES = [
    re.compile("{{[^{}]+}}"),
    re.compile("<ref[^>]*>[^<]*</ref>"),
    re.compile("<ref[^>]+/>"),
    re.compile("<strike>[^<]*</strike>"),
    re.compile("</?br>"),
    re.compile("<!--[^-]+-->"),
    re.compile("<[>]+>"),
    re.compile("^[*#;:]+"),
    re.compile("（）"),
    re.compile("[(][)]"),
    re.compile("^.*[^。]$"),  # 。で終わらない行は削除
]
# 改行文字
BR = "\n"
# 文の終了文字
PERIOD = "。"
# 次の文字を含む行は削除
INVALID_STR = ["ファイル:", "{", "}", "'", "[", "]", "<", ">", "*", "|"]
# 次の文字をタイトル含むページは削除; 一覧ページは残した
INVALID_TITLES = ["(曖昧さ回避)"]


parser = HTMLParser()


# http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
def fast_iter(context, func):
    for event, elem in context:
        func(elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    del context


def process_page(page):
    # 通常の記事のみに限定
    if page.find('{http://www.mediawiki.org/xml/export-0.10/}ns').text != '0':
        return

    # 曖昧さ回避などのページをスキップ
    title = page.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
    for pattern in INVALID_TITLES:
        if pattern in title:
            return

    text = page.find(
        '{http://www.mediawiki.org/xml/export-0.10/}revision/'
        '{http://www.mediawiki.org/xml/export-0.10/}text'
    ).text

    # 見つからなかったときはスキップ
    if not isinstance(text, str) and not isinstance(text, unicode):
        return

    # 。で終わらない行は削除する
    lines = []
    for line in text.split(BR):
        # [[ページ]] のようなページリンクなどを元に戻す
        for t in SUB_TEMPLATES:
            line = t.sub('\g<1>', line).strip()
        # テンプレート記法などは削除する
        for t in DEL_TEMPLATES:
            line = t.sub('', line).strip()
        lines.append(line)
    text = ''.join(lines)
    # テンプレートの置換ミスがある文を削除
    text = PERIOD.join([line.strip() for line in text.split(PERIOD)
                        if all([p not in line for p in INVALID_STR])])
    # &amp; のような実体参照を戻す
    text = parser.unescape(text)

    if text:
        print(text.encode('utf-8'))


if __name__ == '__main__':
    context = etree.iterparse(sys.argv[1], events=('end',), tag='{http://www.mediawiki.org/xml/export-0.10/}page')
    fast_iter(context, process_page)

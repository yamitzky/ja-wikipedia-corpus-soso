# -*- coding: utf-8 -*-
#--------------------------
# 遅すぎて使ってないよ！
#--------------------------

from __future__ import print_function, unicode_literals

import re

from lxml import etree
from mwlib import uparser
from mwlib.parser import nodes


tree = etree.iterparse("jawiki.xml", events=('end', ))

template = re.compile("{{[^{}]+}}")
repl_templates = [
    re.compile("{{仮リンク[|]([^|]+)[|][^{}]+}}"),
    re.compile("{{lang[|][^|]+[|]([^|{}]+)}}", re.IGNORECASE)
]

for event, page in tree:
    if page.tag != "{http://www.mediawiki.org/xml/export-0.10/}page":
        continue

    if page.find("{http://www.mediawiki.org/xml/export-0.10/}ns").text != "0":
        continue

    text = page.find(
        "{http://www.mediawiki.org/xml/export-0.10/}revision/"
        "{http://www.mediawiki.org/xml/export-0.10/}text"
    ).text

    article = uparser.parseString(title="", raw=text)

    corpus = []
    for sec in article.children:
        if not isinstance(sec, nodes.Section):
            continue
        for el in sec.children:
            sec_corpus = []
            paras = [p for p in el.children if isinstance(p, nodes.Paragraph)]
            for para in paras:
                for el in para.children:
                    if isinstance(el, nodes.Text):
                        sec_corpus.append(el.asText())
                        text = el.asText()
                    elif isinstance(el, nodes.ArticleLink) and not el.target.startswith("ファイル:"):
                        sec_corpus.append(el.target)
                        text = el.target
            text = ''.join(sec_corpus)
            for t in repl_templates:
                text = t.sub("\g<1>", text)
            text = template.sub("", text)
            text = text.strip()
            text = "\n".join([line for line in text.split("\n") if line.endswith("。")])
            if '。' not in text or '{' in text or '}' in text:
                continue
            print(text.encode("utf-8"))



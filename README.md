# ja-wikipedia-corpus-soso
日本語ウィキペディアからまぁまぁ綺麗な文章を抽出するプロジェクト

## 使い方

公式のダンプデータの取得

```sh
sh download.sh
```

コーパスの生成

```sh
./parse.py jawiki-latest-pages-meta-current.xml > corpus.txt
```

## サンプルデータ

先頭50行の結果は[sample-50.txt](https://raw.githubusercontent.com/yamitzky/ja-wikipedia-corpus-soso/master/sample-50.txt)にあります。「１行１ページ」の構造になっています。

## ライセンス

sample-50.txtやコーパスの結果はWikipediaと同様「[Creative Commons Attribution-ShareAlike 3.0 Unported License](https://ja.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License)」となりますが、ソースコードは[MIT License](https://github.com/yamitzky/ja-wikipedia-corpus-soso/blob/master/LICENSE)で公開しています

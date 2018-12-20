arabic_dash_formatter
===

## 説明
- OpenXMLのページ番号フィールドを変換します
- "- PAGE -" の文字列を "PAGE /* ArabicDash" に変換します

## 変換対象
```
○: - PAGE - 
○: -    PAGE -
○: - PAGE    -
✗: - A PAGE -
```


## 使い方
```
from arabic_dash_formatter import formatting_page_no

# ファイルパスを与えると変換した文字列を返す
footer_xml = formatting_page_no("test/resources/footer1.xml")

# 変換しない場合は、Noneを返します
print(footer_xml)
```
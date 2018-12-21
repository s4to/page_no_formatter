# coding: utf-8

from bs4 import BeautifulSoup
import re

FORMAT_TAG = "instrText"
ALLOW_OPTION = "MERGEFORMAT"
CONVERT_STRING = re.compile(r" *- *")
ALLOW_STRING = " "
ARABIC_OPTION = " ArabicDash "


def find_fldChar_range(elm):
    """
    fldCharの開始と終了の要素を探す
    """

    prev_elm = next_elm = elm
    begin_elm = None
    end_elm = None

    # 開始位置の取得
    while True:
        prev_elm = prev_elm.previous_sibling

        if not prev_elm:
            return None, None

        begin_elm = contains_field_char(prev_elm, "begin")

        if begin_elm:
            break

    # 停止位置の取得
    separate_attr = False
    while True:
        next_elm = next_elm.next_sibling
        
        if not next_elm:
            return None, None

        if not separate_attr:
            if contains_field_char(next_elm, "separate") is not None:
                separate_attr = True
        else:
            end_elm = contains_field_char(next_elm, "end")

        if end_elm:
            break

    return begin_elm, end_elm


def contains_field_char(elm, attr_val):
    """
    fldCharタグを含んでいれば返す
    Args:
        elm: 検索するXMLの要素
        attr_val: 属性の値と一致するか判定する文字列
    Returns:
        elm: fldCharタグでかつ、指定の属性を持っていれば要素を返す
    """

    fld_char = elm.find("fldChar", recursive=False)

    if not fld_char:
        return None

    field_attr = "w:fldCharType"

    # タグに ":" を含むとfind, selectできないので、属性を取得して処理していく
    for k, v in fld_char.attrs.items():
        if k == field_attr and v == attr_val:
            return elm

    return None


def contains_prev_inlinetext(elm):
    """
    手前の兄弟要素の inline text を処理
    """

    prev_elm = elm
    prev_convert_no = 0

    while True:
        prev_elm = prev_elm.previous_sibling
        res, prev_convert_no = contains_arabic_element(prev_elm, prev_convert_no)

        if not res:
            break

    return prev_elm, prev_convert_no


def contains_next_inlinetext(elm):
    """
    次の兄弟要素の inline text を処理
    """
    next_elm = elm
    next_convert_no = 0

    while True:
        next_elm = next_elm.next_sibling
        res, next_convert_no = contains_arabic_element(next_elm, next_convert_no)

        if not res:
            break

    return next_elm, next_convert_no


def contains_arabic_element(elm, convert_no):
    """
    arabic 要素を含んでいる位置を特定する
    Args:
        elm: XMLの要素
        convert_no: 位置
    Returns:
        bool: 次のelementを処理するかどうか
        int: 整形する可能性のある番号
    """

    # 直前のタグが存在しない、もしくは、rタグでない場合そく終了する
    if not elm or elm.name != "r":
        return False, 0

    inline_text = elm.find("t", recursive=False)
    if not inline_text:
        return False, 0

    # インナーテキストが空の場合、半角スペースとして認識するよう
    if inline_text.string == ALLOW_STRING:
        convert_no += 1
        return True, convert_no

    # ダッシュが含まれるかどうか
    if CONVERT_STRING.fullmatch(inline_text.string):
        convert_no += 1
        return False, convert_no
    else:
        return False, 0


def convert_page_no(prev_elm, prev_no, next_elm, next_no, elm):
    """
    PAGE フィールドを変換する
    XMLの構造が変わる
    """
    for _ in range(prev_no):
        e = prev_elm
        prev_elm = prev_elm.next_sibling
        e.decompose()

    for _ in range(next_no):
        e = next_elm
        next_elm = next_elm.previous_sibling
        e.decompose()

    field = elm.string.split("\*")
    field.insert(1, ARABIC_OPTION)

    elm.string = "\*".join(field)


def convert_element(instrText):
    """
    inStrText要素を変換させる
    Args:
        instrText: inStrText タグ
    Returns:
        bool: 変換したかどうか
    """

    if not instrText.string.find(r"\ PAGE\ "):
        return False

    # 余計なオプションが付いていたら処理しない
    for option in instrText.string.split(r"\*")[1:]:
        if option.find(ALLOW_OPTION) == -1:
            return False

    page_no_elm = instrText.parent

    # 開始位置と終了位置を取得する
    begin_elm, end_elm = find_fldChar_range(page_no_elm)

    # 想定外のfldCharははじく
    if begin_elm is None or end_elm is None:
        return False

    prev_elm, prev_no = contains_prev_inlinetext(begin_elm)
    next_elm, next_no = contains_next_inlinetext(end_elm)

    if prev_no == 0 or next_no == 0:
        return False

    convert_page_no(prev_elm, prev_no, next_elm, next_no, instrText)

    return True


def convert_arabic_dash(file_path):
    """
    XMLの PAGE フィールドが - (dash) で囲まれていた場合変換する
    Args:
        file_path: XMLのファイルパス
    Returns:
        str: XML
    """

    with open(file_path, 'r') as f:
        _xml = f.read()

    try:
        soup = BeautifulSoup(_xml, "xml")

        if soup.find("ftr") is None:
            return None

        # すべてのw:instrTextを対象とする
        instrTexts = soup.find_all(FORMAT_TAG)
        is_convert = False

        for instrText in instrTexts:
            res = convert_element(instrText)

            if res:
                is_convert = True

        if is_convert:
            return str(soup)
        else:
            return None

    except Exception as e:
        return None

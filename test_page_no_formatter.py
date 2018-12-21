# coding: utf-8

from page_no_formatter import convert_arabic_dash
import shutil
import filecmp


def test(file_name):
    # Test
    resources_dir = "test/resources/"
    results_dir = "test/results/"
    true_dir = "test/true/"

    footer = convert_arabic_dash(resources_dir + file_name)

    if footer is None:
        shutil.copyfile(resources_dir + file_name, results_dir + file_name)
    else:
        with open(results_dir + file_name, 'w') as _f:
            _f.write(footer)

    assert(filecmp.cmp(results_dir + file_name, true_dir + file_name))


def main():

    # pdf to docx -> case: -  PAGE -
    pdf_to_docx_footer = "footer1.xml"
    test(pdf_to_docx_footer)

    # PAGEの両端にダッシュを含む
    dash_footer = "footer2.xml"
    test(dash_footer)

    # ページ番号を含まない
    nopage_field = "nopage_field.xml"
    test(nopage_field)

    # - <rタグ以外> PAGE -
    include_nonr_tag = "include_non-r_tag.xml"
    test(include_nonr_tag)

    # -S PAGE - 不正なフォーマット
    between_string = "between_string.xml"
    test(between_string)

    # - PAGE /* OPTION -
    option = "option.xml"
    test(option)

    # footer.xmlでない
    non_footer = "non-footer.xml"
    test(non_footer)


if __name__ == '__main__':
    main()

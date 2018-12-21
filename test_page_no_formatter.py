# coding: utf-8

from page_no_formatter import arabic_dash_converter
import shutil


def main():

    # Test
    import filecmp
    resources_dir = "test/resources/"
    results_dir = "test/results/"
    true_dir = "test/true/"

    # pdf to docx -> case: -  PAGE -
    pdf_to_docx_footer = "footer1.xml"
    footer = arabic_dash_converter(resources_dir + pdf_to_docx_footer)
    with open(results_dir + pdf_to_docx_footer, 'w') as _f:
        _f.write(footer)

    assert(filecmp.cmp(results_dir + pdf_to_docx_footer, true_dir + pdf_to_docx_footer))

    # PAGEの両端にダッシュを含む
    dash_footer = "footer2.xml"
    footer = arabic_dash_converter(resources_dir + dash_footer)
    with open(results_dir + dash_footer, 'w') as _f:
        _f.write(footer)

    assert(filecmp.cmp(results_dir + dash_footer, true_dir + dash_footer))

    # ページ番号を含まない
    nopage_field = "nopage_field.xml"
    footer = arabic_dash_converter(resources_dir + nopage_field)
    if footer is None:
        shutil.copyfile(resources_dir + nopage_field, results_dir + nopage_field)
    else:
        with open(results_dir + nopage_field, 'w') as _f:
            _f.write(footer)

    assert(filecmp.cmp(results_dir + nopage_field, true_dir + nopage_field))

    # - <rタグ以外> PAGE -
    include_nonr_tag = "include_non-r_tag.xml"
    footer = arabic_dash_converter(resources_dir + include_nonr_tag)
    if footer is None:
        shutil.copyfile(resources_dir + include_nonr_tag, results_dir + include_nonr_tag)
    else:
        with open(results_dir + include_nonr_tag, 'w') as _f:
            _f.write(footer)

    assert(filecmp.cmp(results_dir + include_nonr_tag, true_dir + include_nonr_tag))

    # -S PAGE - 不正なフォーマット
    between_string = "between_string.xml"
    footer = arabic_dash_converter(resources_dir + between_string)
    if footer is None:
        shutil.copyfile(resources_dir + between_string, results_dir + between_string)
    else:
        with open(results_dir + between_string, 'w') as _f:
            _f.write(footer)

    assert(filecmp.cmp(results_dir + between_string, true_dir + between_string))


if __name__ == '__main__':
    main()


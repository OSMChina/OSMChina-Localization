import json
from functools import cmp_to_key

syntax_1 = "<!-- MARKDOWN_TABLE_EDITOR BEGIN-->"
syntax_2 = "<!-- WARNING: ALL TABLE ARE MAINTAINED BY PROGRAMME, YOU SHOULD ADD DATA TO COLLECTION JSON -->"
syntax_3 = "<!-- MARKDOWN_TABLE_EDITOR END-->"


def x_sort(data):
    def compare(dict_a: dict, dict_b: dict):
        return 1
    data = sorted(data, key=cmp_to_key(compare))
    return data


def markdown_row(length: int, data: list):
    string = ""
    for i in range(length):
        string += "| " + str(data[i]) + " "
    string += "|\n"
    return string


def markdown_header(translation: dict, locale: str):
    locale_translation = {}
    for i in range(len(translation)):
        if translation[i]["locale"] == locale:
            locale_translation = translation[i]["translation"]
    data = [
        locale_translation["name"],
        locale_translation["website_url"],
        locale_translation["translate_platform"],
        locale_translation["translate_status"],
        locale_translation["translate_link"],
        locale_translation["code_repository"],
        locale_translation["osmwiki_page"],
        locale_translation["contributor"],
    ]
    return markdown_row(len(data), data)


def markdown_table(length: int):
    data = ["-", "-", "-", "-", "-", "-", "-", "-"]
    return markdown_row(length, data)


def markdown_entry(content_entry: dict):
    data = [
        content_entry["name"],
        content_entry["website_url"],
        content_entry["translate_platform"],
        content_entry["translate_status"],
        content_entry["translate_link"],
        content_entry["code_repository"],
        content_entry["osmwiki_page"],
        content_entry["contributor"],
    ]
    return markdown_row(len(data), data)


def markdown_gen(locale: str):
    content_json = open("..\\data\\content_editor.json", "r", encoding="utf-8")
    content_data = json.loads(content_json.read())["EDITOR"]
    column_json = open("..\\data\\column_editor.json", "r", encoding="utf-8")
    column_data = json.loads(column_json.read())
    string = ""
    if locale != "Default":
        string += markdown_header(column_data["i18n"], locale)
    else:
        string += markdown_header(column_data["i18n"], "zh-CN")
    string += markdown_table(
        column_data["len"],
    )
    # content_data.sort(key=lambda x: x["basic_website_name"])
    content_data = x_sort(content_data)
    for i in range(len(content_data)):
        string += markdown_entry(content_data[i])
    return string


def markdown_body(locale, text, token_begin, token_warn, token_end):
    readme_slice = text.split(token_begin)
    readme_slice.append(readme_slice[1].split(token_warn)[0])
    readme_slice.append(readme_slice[1].split(token_end)[1])
    table = markdown_gen(locale)
    markdown = (
        readme_slice[0]
        + token_begin
        + "\n"
        + token_warn
        + "\n"
        + table
        + "\n"
        + token_end
        + readme_slice[3]
    )
    if table == "":
        return text
    else:
        return markdown


def readme_gen(readme_locale):
    if readme_locale != "":
        path = "..\\README" + "-" + readme_locale + ".md"
    else:
        readme_locale = "Default"
        path = "..\\README.md"
    readme_file = open(path, "r", encoding="utf-8")
    readme_text = readme_file.read()
    readme_file.close()
    readme_text = markdown_body(
        readme_locale, readme_text, syntax_1, syntax_2, syntax_3
    )
    readme_file = open(path, "w", encoding="utf-8")
    readme_file.write(readme_text)
    readme_file.close()
    print(readme_locale, ": ", path.replace("..\\", "").replace("../", ""))


readme_gen("")
# readme_gen("zh-CN")
# readme_gen("en-US")

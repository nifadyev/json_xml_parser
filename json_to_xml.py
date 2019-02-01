# -*- coding: utf-8 -*-
from json import load
import requests


def parse(path_to_input_file, path_to_output_file, root="query"):
    result_list = list()

    result_list.append('''<?xml version="1.0" encoding="UTF-8"?>''')
    result_list.append("<%s>" % (root))

    with open(path_to_input_file, "r") as input_file:
        loaded_json = load(input_file)
        for tag_name in loaded_json:
            result_list.append("<%s>%s</%s>" %
                               (tag_name, loaded_json[tag_name], tag_name))

    result_list.append("</%s>" % (root))

    with open(path_to_output_file, "w+") as output_file:
        output_file.write("".join(result_list))

def parse_using_url(url_to_input_file, path_to_output_file, root="query"):
    result_list = list()

    result_list.append('''<?xml version="1.0" encoding="UTF-8"?>''')
    result_list.append("<%s>" % (root))

    loaded_json = requests.get(url_to_input_file).json()
    for tag_name in loaded_json:
        result_list.append("<%s>%s</%s>" %
                            (tag_name, loaded_json[tag_name], tag_name))

    result_list.append("</%s>" % (root))

    if path_to_output_file == "":
        path_to_output_file = "output_xml.xml"

    with open(path_to_output_file, "w+") as output_file:
        output_file.write("".join(result_list))


parse("input_json.json", "output_xml.xml")
parse_using_url("http://ip-api.com/json/%7Bip%7D", "123.xml")

# -*- coding: utf-8 -*-
from json import load
# from dicttoxml import dicttoxml


def parse(path_to_input_file, path_to_output_file, root="query"):
    result_list = list()

    result_list.append('''<?xml version="1.0" encoding="UTF-8"?>''')
    result_list.append("<%s>" % (root))

    with open(path_to_input_file, "r") as input_file:
        loaded_json = load(input_file)
        for tag_name in loaded_json:
            result_list.append("<%s>%s</%s>" %
                               (tag_name, loaded_json[tag_name], tag_name))

        # JSON -> XML using external module dicttoxml
        # xml = dicttoxml(loaded_json, root=True,
        #                 custom_root="query", attr_type=False)
        # with open(path_to_output_file, "wb") as output_file:
        #     output_file.write(xml)

    result_list.append("</%s>" % (root))

    with open(path_to_output_file, "w+") as output_file:
        output_file.write("".join(result_list))


parse("input_json.json", "output_xml.xml")

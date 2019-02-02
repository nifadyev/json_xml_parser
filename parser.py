from json import dump
from lxml import objectify
import requests


class JsonXmlParser:
    '''Parser for XML and JSON files, loaded from specified link'''

    def __init__(self, link, output_format, output_path="output"):
        self.link = link
        self.output_format = output_format
        self.output_path = output_path if output_path != "output" else (
            output_path + "." + output_format)

    def parse(self):
        '''Parse file in order to its format'''

        if self.output_format == "json":
            self.__parse_xml()
        elif self.output_format == "xml":
            self.__parse_json()

    def __parse_xml(self):
        root = objectify.XML(requests.get(self.link).content)
        data = {}

        for node in root.getchildren():
            data[node.tag] = node.text

        with open(self.output_path, "w+") as output_file:
            dump(data, output_file)

    def __parse_json(self):
        root = "query"
        result_list = list()

        result_list.append('''<?xml version="1.0" encoding="UTF-8"?>''')
        result_list.append("<%s>" % (root))
        loaded_json = requests.get(self.link).json()
        for tag_name in loaded_json:
            result_list.append("<%s>%s</%s>" %
                               (tag_name, loaded_json[tag_name], tag_name))
        result_list.append("</%s>" % (root))

        with open(self.output_path, "w+") as output_file:
            output_file.write("".join(result_list))

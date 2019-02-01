# -*- coding: utf-8 -*-
from lxml import objectify
from json import dump
from urllib.request import urlopen


def parse(url_to_xml, path_to_output_file):
    root = objectify.XML(urlopen(url_to_xml).read())
    data = {}

    for element in root.getchildren():
        data[element.tag] = element.text

    with open(path_to_output_file, "w+") as output:
        dump(data, output)


parse("http://ip-api.com/xml/{ip}", "output_json.json")

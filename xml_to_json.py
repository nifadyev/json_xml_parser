# -*- coding: utf-8 -*-
from lxml import objectify
from json import dump
import requests


def parse(url_to_xml, path_to_output_file):
    root = objectify.XML(requests.get(url_to_xml).content)
    data = {}

    for element in root.getchildren():
        data[element.tag] = element.text

    if path_to_output_file == "":
        path_to_output_file ="output_json.json"

    with open(path_to_output_file, "w+") as output:
        dump(data, output)

parse("http://ip-api.com/xml/{ip}", "output_json.json")

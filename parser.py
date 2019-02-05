from json import dump
from lxml import objectify
from requests import get
from lxml import etree


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
        root = objectify.XML(get(self.link).content)
        data = {}

        data[root.tag] = self.to_json(root.getchildren())
        # for node in root.getchildren():
        #     data[node.tag] = node.text if node.text != "" else ""

        with open(self.output_path, "w+") as output_file:
            dump(data, output_file)

    def __parse_json(self):
        with open(self.output_path, "w+") as output_file:
            data = get(self.link).json()
            # parent = etree.Element("query")
            output_file.write(self.to_xml(
                data, None, etree.Element(next(iter(data)))))
        # with open(self.output_path, "r") as output_file:
        #     print(output_file.read())

    def to_json(self, root):
        '''Recursively creates dictionary from xml file'''

        data = {}

        for node in root:
            if node.getchildren():
                data[node.tag] = self.to_json(node.getchildren())
            else:
                if data.get(node.tag):
                    data[node.tag] += [node.text]
                else:
                    data[node.tag] = [node.text] if node.text else [""]

        # Delete extra symbols [] from resulting dictionary
        for key, value in data.items():
            if len(value) == 1 and isinstance(value, dict):
                data[key] = value[0]
        return data

    def to_xml(self, dictionary, parent, root):
        '''Recursively creates string from dictionary received from json file'''
        if parent == None:
            p_parent = etree.Element("query")
            etree.SubElement(p_parent, root.tag)
            # self.to_xml(dictionary, p_parent, root)
            self.to_xml(dictionary, p_parent, p_parent)
            return etree.tostring(p_parent, xml_declaration=True, encoding="utf-8", pretty_print=True).decode("utf-8")

        for key, value in dictionary.items():
            if isinstance(value, dict):
                child = etree.SubElement(root, next(iter(value)))
                self.to_xml(value, root, child)
            elif root.text == None and root.getchildren() == []:
                root.text = str(value)
            else:
                if root.findall(key):
                    root.findall(key)[0].text = str(value)
                else:
                    child = etree.SubElement(parent, key)
                    child.text = str(value)

        return etree.tostring(root, xml_declaration=True, encoding="utf-8", pretty_print=True).decode("utf-8")

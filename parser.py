from json import dump
from lxml import objectify
from requests import get
from lxml import etree


class JsonXmlParser:
    '''Parser for XML and JSON files, loaded from specified link'''

    def __init__(self, link, output_format, output_path="output"):
        self.link = link
        self.output_format = output_format
        self.output_path = (
            output_path + "." + output_format) if output_path == "output" else output_path

    def parse(self):
        '''Parse file in order to its format'''

        if self.output_format == "json":
            self.write_to_json()
        elif self.output_format == "xml":
            self.write_to_xml()

    def write_to_json(self):
        ''' '''

        root = objectify.XML(get(self.link).content)
        data = {}

        # root.getchildren() is depricated 
        data[root.tag] = self.parse_xml(root.getchildren())
        # TODO: with using list(root) behaviour is differ
        # json has got extra root node
        # data[root.tag] = self.parse_xml(list(root))

        with open(self.output_path, "w+") as output_file:
            dump(data, output_file)

    def write_to_xml(self):
        ''' '''

        with open(self.output_path, "w+") as output_file:
            data = get(self.link).json()
            data_with_root = data if isinstance(
                data[next(iter(data))], dict) else {"query": data}

            output_file.write(self.parse_json(
                data_with_root, None, etree.Element(next(iter(data_with_root)))))

        with open(self.output_path, "r") as output_file:
            print(output_file.read())

    def parse_xml(self, root):
        '''Recursively creates dictionary from xml file'''

        data = {}

        for node in root:
            child = node.getchildren()
            # child = list(node)
            if child:
                data[node.tag] = self.parse_xml(child)
            elif node.tag in data:
                data[node.tag] += [node.pyval]
            else:
                data[node.tag] = [node.pyval] if node.text else [""]

        # Delete extra symbols [] from resulting dictionary
        for key, value in data.items():
            if len(value) == 1 and isinstance(value, list):
                data[key] = value[0]

        return data

    def parse_json(self, dictionary, parent, root):
        '''Recursively fill etree.
            Return formatted string
        '''

        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.parse_json(value, root, etree.SubElement(
                    root, next(iter(value))))
            # Fill most distant from parent leaf
            # elif root.text == None and root.getchildren() == []:
            elif root.text is None and not root.getchildren():
                root.text = str(value)
            # root node is filled, fill his neighbor
            else:
                etree.SubElement(parent, key).text = str(value)

        return etree.tostring(
            root, xml_declaration=True, encoding="utf-8", pretty_print=True).decode("utf-8")

from json import dump
from lxml import objectify, etree
from requests import get


class JsonXmlParser:
    """Parse XML and JSON files, loaded from specified link.
        Write parsed data to file.
    """

    def __init__(self, link, output_format, output_path="output"):
        self.link = link
        self.output_format = output_format
        self.output_path = "".join(
            [output_path, ".", output_format] if output_path == "output" else [output_path])

    def parse(self):
        """Call suitable function to parse input file."""

        self.write_to_json() if self.output_format == "json" else self.write_to_xml()

    def write_to_json(self):
        """Load xml file and write parsed data to output file."""

        root = objectify.XML(get(self.link).content)

        with open(self.output_path, "w+") as output_file:
            dump(self.parse_xml(list(root)), output_file)

    def write_to_xml(self):
        """Load json file and write parsed data to output file."""

        with open(self.output_path, "w+") as output_file:
            data = get(self.link).json()

            # Artificially create extra dictionary for json files without root node
            data_with_root = data if isinstance(
                data[next(iter(data))], dict) else {"query": data}

            output_file.write(self.parse_json(
                data_with_root, None, etree.Element(next(iter(data_with_root)))))

    def parse_xml(self, root):
        """Parse xml file to dictionary.

        Returns:
            dict -- parsed data loaded from link to xml file
        """

        data = {}

        for node in root:
            child = node.getchildren()
            if child:
                if isinstance(root, list) and node.tag not in data:
                    data[node.tag] = [self.parse_xml(child)]
                else:
                    data[node.tag].append(self.parse_xml(child))
            elif node.tag in data:
                data[node.tag].extend(node.text)
            else:
                data[node.tag] = [node.text] if node.text else [""]

        # Delete extra symbols [] from resulting dictionary if list of values constains only 1 value
        for key, value in data.items():
            if len(value) == 1 and isinstance(value, list):
                data[key] = value[0]

        return data

    def parse_json(self, dictionary, parent, root):
        """Parse json file to string using ElementTree

        Returns:
            string -- formatted string with xml declaration and encoding
        """

        for key, value in dictionary.items():
            # Current root node has nested nodes
            if isinstance(value, dict):
                self.parse_json(value, root, etree.SubElement(
                    root, next(iter(value))))
            # Fill most distant from parent leaf
            elif root.text is None and not root.getchildren():
                root.text = str(value)
            # Root node has value, fill his neighbor
            else:
                etree.SubElement(parent, key).text = str(value)

        return etree.tostring(
            root, xml_declaration=True, encoding="utf-8", pretty_print=True).decode("utf-8")

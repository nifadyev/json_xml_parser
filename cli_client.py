"""2 программы. которые принимают аргументы от 
юзера(адрес) и возвращают в нужном формате. одна запрашивает
xml и вовзращает json, вторая наоборот """
from xml_to_json import parse as parse_to_json
from json_to_xml import parse_using_url as parse_to_xml


def cli():
    operation = input("Enter the format of output file (xml/json): ")
    url_to_input_file = input("Please enter the address to input file: ")
    # TODO: add ArgumentParser

    path_to_output_file = input(
        "Please enter the path to output file (path.json/path.xml) or leave it empty: ")

    if operation == "json":
        parse_to_json(url_to_input_file, path_to_output_file)
    elif operation == "xml":
        parse_to_xml(url_to_input_file, path_to_output_file)


cli()

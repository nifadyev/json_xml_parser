"""2 программы. которые принимают аргументы от 
юзера(адрес) и возвращают в нужном формате. одна запрашивает
xml и вовзращает json, вторая наоборот """
from xml_to_json import parse as parse_to_json
from json_to_xml import parse_using_url as parse_to_xml
from argparse import ArgumentParser
from requests import get


def main(link, operation, output_path=""):
    if operation == "json":
        parse_to_json(link, output_path)
    elif operation == "xml":
        parse_to_xml(link, output_path)


arg_parser = ArgumentParser()
arg_parser.add_argument("link", help="link to input file")
arg_parser.add_argument(
    "format", help="format output file", choices=["json", "xml"])
arg_parser.add_argument(
    "-out", "--output", help="path to output file", metavar="")
args = arg_parser.parse_args()

if get(args.link).status_code != 200:
    raise ValueError("Link is broken or doesn't contain file")

if __name__ == '__main__':
    main(args.link, args.format, args.output if args.output else "")

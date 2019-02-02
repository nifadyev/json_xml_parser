from parser import JsonXmlParser
from argparse import ArgumentParser
from requests import get


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("link", help="link to input file")
    arg_parser.add_argument(
        "format", help="format output file", choices=["json", "xml"])
    arg_parser.add_argument(
        "-out", "--output", help="path to output file", metavar="", default="")
    args = arg_parser.parse_args()

    if get(args.link).status_code != 200:
        raise ValueError("Link is broken or doesn't contain file")

    JsonXmlParser(args.link, args.format, args.output).parse()


if __name__ == '__main__':
    main()
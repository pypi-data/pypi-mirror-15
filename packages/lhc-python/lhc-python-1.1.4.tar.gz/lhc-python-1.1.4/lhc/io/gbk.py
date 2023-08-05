__author__ = 'Liam Childs'

if __name__ == '__main__' and __package__ is None:
    import lhc.io
    __package__ = 'lhc.io'

import argparse

from .gbk_ import GbkIterator, GbkSequenceSet
from .gbk_.tools import extract, split


def main():
    args = get_parser().parse_args()
    args.func(args)


def get_parser():
    return define_parser(argparse.ArgumentParser())


def define_parser(parser):
    subparsers = parser.add_subparsers()
    extract_parser = subparsers.add_parser('extract')
    extract.define_parser(extract_parser)
    split_parser = subparsers.add_parser('split')
    split.define_parser(split_parser)
    return parser


if __name__ == '__main__':
    import sys
    sys.exit(main())

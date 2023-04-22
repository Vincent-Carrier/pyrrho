import argparse

from treebank import parse_treebank

parser = argparse.ArgumentParser(description='Syntax highlight a treebank.')
parser.add_argument('file', type=str, help='treebank file')
parser.add_argument('-s',
                    '--start',
                    type=int,
                    default=0,
                    required=False,
                    help='sentence start index')
parser.add_argument('-e',
                    '--end',
                    type=int,
                    default=-1,
                    required=False,
                    help='sentence end index')
parser.add_argument('-t', '--title', type=str)
parser.add_argument('-a', '--author', type=str)
parser.add_argument('-v', '--verse', type=str)
args = parser.parse_args()

tb = parse_treebank(args.file, args.start, args.end, args.verse or 'prose')
if args.title: tb.title = args.title
if args.author: tb.author = args.author

print(tb)
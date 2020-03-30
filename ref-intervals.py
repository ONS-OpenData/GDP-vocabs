#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description='Create interval labels from a list of interval URIs.')
parser.add_argument('intervals',
                    nargs='?',
                    help='File with one URI per line',
                    type=argparse.FileType('r'),
                    default=sys.stdin)

args = parser.parse_args()

REF_ID = 'http://reference.data.gov.uk/id/'

# from https://stackoverflow.com/questions/597476/how-to-concisely-cascade-through-multiple-regex-statements-in-python

import re

class Re(object):
  def __init__(self):
    self.last_match = None
  def fullmatch(self,pattern,text):
    self.last_match = re.fullmatch(pattern,text)
    return self.last_match

QUARTER = re.compile(r'quarter/(.*)')
GREG_DATE_PERIOD = re.compile(r'gregorian-interval/([0-9]{4}-[0-9]{2}-[0-9]{2})T00:00:00/(.*)')

for line in args.intervals:
    line = line.strip()
    if line.startswith(REF_ID):
        line = line[len(REF_ID):]
    gre = Re()
    if gre.fullmatch(QUARTER, line):
        q,  = gre.last_match.groups()
        print(f'<{REF_ID}{line}> <http://www.w3.org/2000/01/rdf-schema#label> "{q}" .')
    elif gre.fullmatch(GREG_DATE_PERIOD, line):
        year, period = gre.last_match.groups()
        print(f'<{REF_ID}{line}> <http://www.w3.org/2000/01/rdf-schema#label> "{year} {period}" .')
    else:
        print(f'Unknown {line}')

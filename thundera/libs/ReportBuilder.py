import os
import re
import time
import magic
import mimetypes
import hashlib
import tarfile
import gzip
import csv
import sys
import mmap
import json
import string
from datetime import date


class ReportBuilder:

    def __init__(self, report_format):
        self.format = report_format
        self.files = {}
        self.matches = {}
        self.rules = {}

    def summary(self, filelist, exfilelist, procfiles):
        print('')
        print('Summary:')
        print("  Scanned:", len(filelist), 'files')
        print("  Excluded:", len(exfilelist), 'files')
        print("  Processed:", len(procfiles), 'files')
        print('')

    def print_files(self):
        print('')
        print('Files:')
        for checksum in self.files:
            taglabel = "["+checksum+"]:"
            print(
                ' ',
                taglabel,
                self.files[checksum]['filepath'],
                len(self.files[checksum]['symbols']),
                'symbols')
        print('')

    def print_matches(self):
        print('')
        print('Matches:')
        for checksum in self.matches:
            package = self.rules[checksum]['package']
            license = self.rules[checksum]['license']
            print(' ', package, '('+license+'):')
            for match in self.matches[checksum]:
                print('  ', match)
        print('')

    def print_rule(self, symbols):
        for symbol in symbols:
            if len(symbol) <= 2:
                symbols.remove(symbol)
            elif '.' in symbol:
                new_sym = symbol.split('.')
                symbols.append(new_sym[0])
                symbols.remove(symbol)
        today = date.today()
        fdate = today.strftime("%Y-%m-%d")
        rule_json = {
            "publisher": "<PUBLISHER>",
            "updated": fdate,
            "package": "<PACKAGE_NAME>",
            "license": "<SPDX>",
            "symbols": symbols
        }
        json_object = json.dumps(rule_json, indent=4)
        print(json_object)

    def add_rules(self, rules):
        self.rules = rules

    def add_file(self, checksum, filepath, symbols):
        self.files[checksum] = {'filepath': filepath, 'symbols': symbols}

    def add_matches(self, matches):
        self.matches = matches

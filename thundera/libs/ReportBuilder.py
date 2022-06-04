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

class ReportBuilder:

    def __init__(self, report_type, report_format):
        self.type = report_type
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
            print(' ',
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
            print(' ',
                package,
                '('+license+'):')
            for match in self.matches[checksum]:
                print('  ', match)

        print('')

    def add_rules(self, rules):
        self.rules = rules

    def add_file(self, checksum, filepath, symbols):
        self.files[checksum] = {'filepath':filepath, 'symbols':symbols}

    def add_matches(self, matches):
        self.matches = matches

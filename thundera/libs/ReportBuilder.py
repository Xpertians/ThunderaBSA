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
import io
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
        if len(self.matches) >= 1:
            for checksum in self.matches:
                package = self.rules[checksum]['package']
                license = self.rules[checksum]['license']
                print(' ', package, '('+license+'):')
                self.export_matches()
                if len(self.matches[checksum]) <= 10:
                    for match in self.matches[checksum]:
                        print('  ', match)
                else:
                    print('  ', 'over', len(self.matches[checksum]), 'matches')
        else:
            print(' ', 'No matches')
        print('')

    def export_matches_csv(self, csv_data):
        fname = './thundera-matches.csv'
        csv_columns = ['Rule','Package','License', 'File', 'Matches']
        try:
            writer = csv.writer(
                open(fname,"w"),
                delimiter=',',
                quoting=csv.QUOTE_ALL)
            writer.writerow(csv_columns)
            for rule_id in csv_data:
                for match in csv_data[rule_id]['matches']:
                    row = [
                        rule_id,
                        csv_data[rule_id]['package'],
                        csv_data[rule_id]['license'],
                        match['filepath'],
                        ",".join(match['matches'])
                    ]
                    writer.writerow(row)
        except IOError:
            print("I/O error")

    def export_matches_json(self, json_data):
        fname = './thundera-matches.json'
        json_object = json.dumps(json_data, indent=4)
        with io.open(fname, 'w', encoding='utf-8') as f:
            f.write(json_object)

    def export_matches(self):
        mreport = {}
        for checksum in self.matches:
            package = self.rules[checksum]['package']
            license = self.rules[checksum]['license']
            mreport[checksum] = {
                'package': self.rules[checksum]['package'],
                'license': self.rules[checksum]['license'],
                'matches': self.matches[checksum]
            }
        # self.export_matches_json(mreport)
        self.export_matches_csv(mreport)

    def export_rule(self, symbols, filter_str):
        cleanSyms = []
        for symbol in symbols:
            symbol.strip()
            if '.' in symbol:
                new_sym = symbol.split('.')
                symbol = new_sym[0]
            if len(symbol) >= 2:
                if len(filter_str) <= 1:
                    cleanSyms.append(symbol)
                else:
                    if re.search(filter_str, symbol, flags=re.IGNORECASE):
                        cleanSyms.append(symbol)

        today = date.today()
        fdate = today.strftime("%Y-%m-%d")
        rule_json = {
            "publisher": "<PUBLISHER>",
            "updated": fdate,
            "package": "<PACKAGE_NAME>",
            "license": "<SPDX>",
            "symbols": cleanSyms
        }
        json_object = json.dumps(rule_json, indent=4)
        fname = 'outpost-rules.json'
        with io.open(fname, 'w', encoding='utf-8') as f:
            f.write(json_object)
        checksum = self.get_checksum(fname)
        filename = checksum+'-rules.json'
        os.rename(fname, filename)
        print('Rules:')
        print(' ', 'Rule file created:', filename)

    def add_rules(self, rules):
        self.rules = rules

    def add_file(self, checksum, filepath, symbols):
        self.files[checksum] = {'filepath': filepath, 'symbols': symbols}

    def add_matches(self, matches):
        self.matches = matches

    def get_checksum(self, filepath):
        with open(filepath, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()

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
            print(taglabel, self.files[checksum]['filepath'])
        print('')

    def add_file(self, checksum, filepath, symbols):
        print('checksum:', checksum)
        print('filepath:', filepath)
        print('symbols:', symbols)
        self.files[checksum] = {'filepath':filepath, 'symbols':symbols}

    def add_matches(self, checksum, filepath, symbols):
        print('checksum:', checksum)
        print('filepath:', filepath)
        print('symbols:', symbols)
        self.matches[checksum] = {'filepath':filepath, 'symbols':symbols}

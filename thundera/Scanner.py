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
import tarfile
import zipfile
from slugify import slugify
from zipfile import ZipFile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from thundera.libs import ErrorHandler
from thundera.libs import FileHandler
from thundera.libs import RulesHandler


class Scanner:

    def __init__(self, errorHandler, skipScan, verbose, filelist):
        self.rh = RulesHandler.RulesHandler(errorHandler)
        self.ignore = self.rh.get_ignore()
        self.rules = self.rh.get_rules()
        self.debug = errorHandler
        self.filelist = filelist
        self.exfilelist = []
        self.procfiles = []
        self.report = {}
        self.enumerate_files(filelist)
        symbols = []
        for filepath in self.filelist:
            fileHandler = FileHandler.FileHandler(
                self.debug,
                filepath)
            symbols = fileHandler.run_handler()
            if symbols is None:
                symbols = []
            if isinstance(symbols, str):
                if symbols.find(",") != -1:
                    symbols = symbols.split(',')
                else:
                    symbols = []
            matches = []
            if len(symbols) >= 1:
                symbols = list(filter(lambda i: i not in self.ignore, symbols))
                self.procfiles.append(filepath)
                basename = os.path.basename(filepath)
                basename = os.path.splitext(basename)[0]
                symbols.append(basename)
                print('file:', filepath)
                print('checksum:', fileHandler.exp_checksum())
                print('symbols:', len(symbols))
                print('clean_symbols:', symbols)
                if not skipScan:
                    for rule in self.rules:
                        matches = list(
                            filter(
                                lambda i: i in self.rules[rule]['symbols'],
                                symbols))
                        if len(matches) >= 1:
                            self.report[rule] = matches
                else:
                    print('skipping scan')

            else:
                self.exfilelist.append(filepath)
        print('report:', self.report)
        print("filelist:", len(self.filelist))
        print("exfilelist:", len(self.exfilelist))
        print("procfiles:", len(self.procfiles))

    def enumerate_files(self, filelist):
        sub_flist = []
        for file in filelist:
            if os.path.islink(file):
                self.exfilelist.append(file)
                self.filelist.remove(file)
            else:
                mime = magic.Magic(mime=True)
                filetype = mime.from_file(file)
                if self.is_archive(filetype):
                    new_dir = os.path.splitext(file)[0]
                    if tarfile.is_tarfile(file):
                        self.filelist.remove(file)
                        file = tarfile.open(file)
                        file.extractall(new_dir)
                        file.close()
                    elif zipfile.is_zipfile(file):
                        with ZipFile(file, 'r') as zip_ref:
                            zip_ref.extractall(new_dir)
                            self.filelist.remove(file)
                    else:
                        self.debug.error("Missing Handler for:", filetype)
                        self.debug.error(">", file)
                    for cdp, csb, cfs in os.walk(new_dir):
                        for aFile in cfs:
                            file_path = str(os.path.join(cdp, aFile))
                            filetype = mime.from_file(file_path)
                            self.filelist.append(file_path)
                            if self.is_archive(filetype):
                                sub_flist.append(file_path)
                                self.enumerate_files(sub_flist)

    def is_archive(self, file_type):
        # This function needs improvement
        list_mimes = [
            'application/java-archive',
            'application/zip',
            'application/java-archive',
            'application/gzip',
            'application/zlib',
            'application/x-tar'
            ]
        if file_type in list_mimes:
            return True
        else:
            return False

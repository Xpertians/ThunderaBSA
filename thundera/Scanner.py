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
import shutil
from slugify import slugify
from zipfile import ZipFile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from thundera.libs import ErrorHandler
from thundera.libs import FileHandler
from thundera.libs import RulesHandler
from thundera.libs import ReportBuilder


class Scanner:

    def __init__(self, errorHandler, extract, filter_str, format, filelist):
        self.rh = RulesHandler.RulesHandler(errorHandler)
        self.ignore = self.rh.get_ignore()
        self.rules = self.rh.get_rules()
        self.debug = errorHandler
        self.rp = ReportBuilder.ReportBuilder(format)
        self.filelist = filelist
        self.exfilelist = []
        self.procfiles = []
        self.report = {}
        self.enumerate_files(filelist, 0)
        symbols = []
        self.gsym = []
        for filepath in self.filelist:
            if os.path.islink(filepath):
                self.exfilelist.append(filepath)
            else:
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
                checksum = fileHandler.exp_checksum()
                if len(symbols) >= 1:
                    symbols = list(
                        filter(
                            lambda i: i not in self.ignore,
                            symbols))
                    self.procfiles.append(filepath)
                    basename = os.path.basename(filepath)
                    basename = os.path.splitext(basename)[0]
                    symbols.append(basename)
                    self.rp.add_file(checksum, filepath, symbols)
                    if not extract:
                        for rule in self.rules:
                            matches = list(
                                filter(
                                    lambda i: i in self.rules[rule]['symbols'],
                                    symbols))
                            if len(matches) >= 1:
                                hits = {
                                    'filepath': filepath,
                                    'matches': matches}
                                if rule in self.report:
                                    self.report[rule].append(hits)
                                else:
                                    self.report[rule] = []
                                    self.report[rule].append(hits)
                    else:
                        for symbol in symbols:
                            self.gsym.append(symbol)
                else:
                    self.exfilelist.append(filepath)
        self.rp.add_rules(self.rules)
        self.rp.add_matches(self.report)
        self.rp.summary(self.filelist, self.exfilelist, self.procfiles)
        if not extract:
            self.rp.print_matches()
        else:
            self.rp.export_rule(self.gsym, filter_str)

    def enumerate_files(self, filelist, loop):
        sub_flist = []
        for file in filelist:
            if os.path.islink(file):
                self.exfilelist.append(file)
                self.filelist.remove(file)
            else:
                mime = magic.Magic(mime=True)
                filetype = ''
                try:
                    filetype = mime.from_file(file)
                except (IOError, OSError) as e:
                    self.exfilelist.append(file)
                    self.filelist.remove(file)
                    if e.errno == errno.ENOENT:
                        print('symlink doesnt exist:', file)
                    else:
                        raise e
                if self.is_archive(filetype):
                    # print('is_archive:', file)
                    new_dir = os.path.splitext(file)[0]
                    if os.path.isfile(new_dir):
                        new_dir = new_dir + '_tmp'
                    if tarfile.is_tarfile(file):
                        # print('tarfile:', file)
                        self.filelist.remove(file)
                        file = tarfile.open(file)
                        file.extractall(new_dir)
                        file.close()
                    elif filetype in 'application/zip':
                        # print('zip:', file)
                        with ZipFile(file, 'r') as zip_ref:
                            zip_ref.extractall(new_dir)
                            if file in self.filelist:
                                self.filelist.remove(file)
                            else:
                                self.debug.error(" file not listed:" + file)
                    elif filetype in 'application/gzip':
                        # print('gzip:', file)
                        # Pending Implementation
                        if file in self.filelist:
                            self.filelist.remove(file)
                        else:
                            self.debug.error(" file not listed:" + file)
                    elif filetype in 'application/x-bzip2':
                        # print('bunzip2:', file)
                        # Pending Implementation
                        if file in self.filelist:
                            self.filelist.remove(file)
                        else:
                            self.debug.error(" file not listed:" + file)
                    elif filetype in 'application/x-xz':
                        # print('xz:', file)
                        # Pending Implementation
                        if file in self.filelist:
                            self.filelist.remove(file)
                        else:
                            self.debug.error(" file not listed:" + file)
                    elif filetype in 'application/java-archive':
                        # print('java-archive:', file)
                        # Pending Implementation
                        if file in self.filelist:
                            self.filelist.remove(file)
                        else:
                            self.debug.error(" file not listed:" + file)
                    else:
                        self.debug.error("Missing Archive Handler:" + filetype)
                        self.debug.error(" > " + file)
                    for cdp, csb, cfs in os.walk(new_dir):
                        for aFile in cfs:
                            file_path = str(os.path.join(cdp, aFile))
                            filetype = mime.from_file(file_path)
                            self.filelist.append(file_path)
                            if self.is_archive(filetype):
                                self.filelist.append(file_path)
                                self.enumerate_files(self.filelist, (loop+1))

    def is_archive(self, file_type):
        # This function needs improvement
        list_mimes = [
            'application/java-archive',
            'application/zip',
            'application/java-archive',
            'application/gzip',
            'application/zlib',
            'application/x-tar',
            'application/x-bzip2',
            'application/x-xz'
            ]
        if file_type in list_mimes:
            return True
        else:
            return False

    def is_excluded(self, file_type):
        # This function needs improvement
        list_mimes = [
            'inode/symlink'
            ]
        if file_type in list_mimes:
            return True
        else:
            return False

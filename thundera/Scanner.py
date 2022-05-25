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
import string
import tarfile
import zipfile
from slugify import slugify
from zipfile import ZipFile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from thundera.libs import ErrorHandler
from thundera.libs import FileHandler


class Scanner:

    def __init__(self, errorHandler, filelist):
        self.debug = errorHandler
        self.filelist = filelist
        self.exfilelist = []
        self.enumerate_files(filelist)
        # print("filelist", self.filelist)
        # print("exfilelist", self.exfilelist)
        for filepath in self.filelist:
            # if not self.isarchive and not self.forceign:
            # fCSV = os.path.splitext(filename)[0]
            fileHandler = FileHandler.FileHandler(
                self.debug,
                filepath)
            symbols = fileHandler.run_handler()
            if type(symbols) == str:
                symbols = []
            if symbols is None:
                symbols = []
            if len(symbols) >= 1:
                print('file:', filepath)
                print('checksum:', fileHandler.exp_checksum())
                print('symbols:', len(symbols))

    def enumerate_files(self, filelist):
        sub_flist = []
        for file in filelist:
            if os.path.islink(file):
                self.exfilelist.append(file)
                self.filelist.remove(file)
            else:
                mime = magic.Magic(mime=True)
                filetype = mime.from_file(file)
                # print("file:", file, filetype)
                if self.is_archive(filetype):
                    new_dir = os.path.splitext(file)[0]
                    if tarfile.is_tarfile(file):
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
                        print("Missing Handler for:", filetype)
                        print(">", file)
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

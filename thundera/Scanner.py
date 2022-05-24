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
from slugify import slugify
from zipfile import ZipFile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

class Scanner:

    def __init__(self, debug, filelist):
        self.filelist = filelist
        self.exfilelist = []
        self.enumerate_files(filelist)
        # print("filelist", self.filelist)
        # print("exfilelist", self.exfilelist)
        for filepath in self.filelist:
            print("file:", filepath)
            self.process_file(filepath)

    def enumerate_files(self, filelist):
        sub_flist = []
        for file in filelist:
            # exclude symlinks
            if os.path.islink(file):
                self.exfilelist.append(file)
                self.filelist.remove(file)
            else:
                mime = magic.Magic(mime=True)
                filetype = mime.from_file(file)
                if self.is_archive(filetype):
                    looping = True
                    with ZipFile(file, 'r') as zip_ref:
                        zip_dir = os.path.splitext(file)[0]
                        zip_ref.extractall(zip_dir)
                        self.filelist.remove(file)
                        for cdp, csb, cfs in os.walk(zip_dir):
                            for aFile in cfs:
                                file_path = str(os.path.join(cdp, aFile))
                                filetype = mime.from_file(file_path)
                                self.filelist.append(file_path)
                                if self.is_archive(filetype):
                                    sub_flist.append(file_path)
                                    self.enumerate_files(sub_flist)

    def process_file(self, filepath):
        print("proc:", filepath)
        try:
            fd = open(filepath, "rb")
            data = fd.read().decode("utf-8", "ignore")
            fd.close()
        except:
            print("There was an error opening the file:\n")
            print(filepath)

        count = 0
        window = 5
        charslist = []
        printable = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_/\.,1234567890!@#$%^&*(){}[]"
        for character in data:
            if character in printable:
                charslist.append(character)
                count += 1
            else:
                if count >= window:
                    print(''.join(charslist[-count:]))
                    count = 0
        if count >= window:
            print(''.join(charslist[-count:]))


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

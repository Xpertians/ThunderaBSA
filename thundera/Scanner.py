import os
import time
import magic
import mimetypes
import hashlib
import tarfile
import gzip
import csv
import sys
from slugify import slugify
from zipfile import ZipFile
from pathlib import Path


class Scanner:

    def __init__(self, debug, filelist):
        self.filelist = filelist
        self.exfilelist = []
        self.enumerate_files(filelist)
        print(self.filelist)
        print(self.exfilelist)

    def enumerate_files(self, filelist):
        for file in filelist:
            # exclude symlinks
            if os.path.islink(file):
                self.exfilelist.append(file)
                self.filelist.remove(file)
            else:
                # Quick check for archive file
                # Needs improvement for anidaded zip files
                mime = magic.Magic(mime=True)
                filetype = mime.from_file(file)
                if self.is_archive(filetype):
                    with ZipFile(file, 'r') as zip_ref:
                        zip_dir = os.path.splitext(file)[0]
                        zip_ref.extractall(zip_dir)
                        self.filelist.remove(file)
                        for cdp, csb, cfs in os.walk(zip_dir):
                            for aFile in cfs:
                                file_path = str(os.path.join(cdp, aFile))
                                self.filelist.append(file_path)
            # check subfolders for zip files

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

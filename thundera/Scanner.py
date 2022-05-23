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
        # Quick check for archive file
        for file in filelist:
            print(file)
            print('')
            mime = magic.Magic(mime=True)
            filetype = mime.from_file(file)
            print(filetype)
            if self.is_archive(filetype):
                with ZipFile(file, 'r') as zipObj:
                    listOfiles = zipObj.namelist()
                    print(listOfiles)

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

import os
import lief
import re
import mimetypes
import magic
import hashlib
import os.path
import subprocess
from os import path
from string import digits
from . import ErrorHandler
from . import CtagsHandler


class FileHandler:

    def __init__(self, errorHandler, filepath):
        self.debug = errorHandler
        self.filepath = filepath
        self.filetype = self.get_mime(filepath)
        self.checksum = self.get_checksum(filepath)

    def exp_mime(self):
        return self.filetype

    def exp_checksum(self):
        return self.checksum

    def run_handler(self):
        try:
            handlers = self.preload_handlers()
            handler = handlers[self.filetype]
            return handler(self.filepath, self.checksum)
        except KeyError:
            self.debug.error('handler not implemented for ' + self.filetype)
            self.debug.error('skipping ' + self.filepath)

    def handle_sharedlib(self, filepath, checksum):
        libSO = lief.parse(filepath)
        symbols = []
        iter = filter(lambda e: e.exported, libSO.dynamic_symbols)
        for idx, lsym in enumerate(iter):
            symbols.extend(self.demangle(lsym.name))
        return list(set(symbols))

    def handle_strings(self, filepath, checksum):
        symbols = self.get_strings(filepath)
        return list(set(symbols))

    def handle_objectivec(self, filepath, checksum):
        # needs checking
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('objectivec')
        ctags.setLangMap('objectivec:.h.m')
        return ctags.run()

    def handle_cplusplus(self, filepath, checksum):
        # needs checking
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setOption('--kinds-C++=+l')
        ctags.setOption('-o -')
        return ctags.run()

    def handle_rust(self, filepath, checksum):
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('Rust')
        ctags.setLangMap('Rust:.rs')
        return ctags.run()

    def handle_java(self, filepath, checksum):
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('Java')
        ctags.setLangMap('java:+.aj')
        return ctags.run()

    def handle_ruby(self, filepath, checksum):
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('ruby')
        ctags.setLangMap('ruby:+.rake')
        return ctags.run()

    def handle_perl(self, filepath, checksum):
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('Perl')
        ctags.setLangMap('Perl:+.t')
        return ctags.run()

    def handle_python(self, filepath, checksum):
        ctags = CtagsHandler.CtagsHandler(filepath)
        ctags.setLang('python')
        ctags.setOption('--python-kinds=-iv')
        return ctags.run()

    def preload_handlers(self):
        # This should be replaced by a BD
        return {
            # Parsing language specific
            'text/x-c': self.handle_cplusplus,
            'text/x-c++': self.handle_cplusplus,
            'text/x-python': self.handle_python,
            'text/x-perl': self.handle_perl,
            'text/x-ruby': self.handle_ruby,
            'text/x-rust': self.handle_rust,
            'text/x-java': self.handle_java,
            'text/x-objective-c': self.handle_objectivec,
            #'application/x-mach-binary': self.handle_mach_o,
            #'application/x-archive': self.handle_ar,

            # Parsing Libs
            'application/x-sharedlib': self.handle_sharedlib,

            # Parsing Strings
            'application/x-dosexec': self.handle_strings,
            'font/sfnt': self.handle_strings,

            # Ignored mimetypes
            'text/plain': self.ignore,
            'text/html': self.ignore,
            'text/x-shellscript': self.ignore,
            'application/octet-stream': self.ignore,
            'application/x-ms-pdb': self.ignore,
            'image/vnd.microsoft.icon': self.ignore,
            'text/x-shellscript': self.ignore,
            'text/xml': self.ignore,
            'application/csv': self.ignore,
            'text/x-tex': self.ignore,
            'text/x-makefile': self.ignore,
            'application/json': self.ignore,
            'text/html': self.ignore,
            'image/x-portable-pixmap': self.ignore,
            'image/webp': self.ignore,
            'image/png': self.ignore,
            'image/svg+xml': self.ignore,
            'image/x-tga': self.ignore,
            'image/g3fax': self.ignore,
            'image/gif': self.ignore,
            'image/jpeg': self.ignore,
            'application/x-wine-extension-ini': self.ignore,
            'audio/mpeg': self.ignore,
            'audio/x-wav': self.ignore,
            'video/mp4': self.ignore,
            'inode/x-empty': self.ignore
        }

    def ignore(self, filepath, checksum):
        self.debug.info('ignoring ' + self.filepath)
        return ''

    def get_strings(self, filepath):
        try:
            fd = open(filepath, "rb")
            data = fd.read().decode("utf-8", "ignore")
            fd.close()
        except:
            self.debug.error("There was an error opening the file:\n")
            self.debug.error(filepath)
        symbols = []
        count = 0
        window = 5
        charslist = []
        printable = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_.1234567890!@$%&*"
        for character in data:
            if character in printable:
                charslist.append(character)
                count += 1
            else:
                if count >= window:
                    symbols.append(''.join(charslist[-count:]))
                    count = 0
        if count >= window:
            symbols.append(''.join(charslist[-count:]))
        return symbols

    def demangle(self, name):
        s = re.sub("[^a-zA-Z]+", ",", name)
        s.replace(',,', ',')
        lst = s.split(",")
        lst = (map(lambda x: x.lower(), lst))
        lst = set(lst)
        return lst

    def get_mime(self, filepath):
        mime = magic.Magic(mime=True)
        return mime.from_file(filepath)

    def get_checksum(self, filepath):
        with open(filepath, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()
import os
import re
import json
import hashlib
import os.path
from os import path
from . import ErrorHandler
import shutil, configparser


class RulesHandler:

    def __init__(self, errorHandler):
        self.debug = errorHandler
        self.ignore = []
        self.rules = {}
        self.rules_path = "rules/"
        self.ign_file = "default_ignore.json"
        self.idx_file = "default_index.json"
        self.usr_cfg_dir = os.path.expanduser("~") + "/.config/thunderabsa"
        self.check_index_file()

    def check_index_file(self):
        usr_cfg = self.usr_cfg_dir + "/" + self.idx_file
        if not os.path.isfile(usr_cfg):
            os.makedirs(self.usr_cfg_dir, exist_ok=True)
            orig_ign_file = os.path.join(
                self.rules_path,
                self.idx_file)
            # Get local copy from rules folder
            df_ign_file = os.path.join(self.rules_path, self.idx_file)
            if os.path.exists(df_ign_file):
                shutil.copyfile(df_ign_file, usr_cfg)
            else:
                self.debug.error('index file not found: ' + ignore_file)

    def load_index(self, data):
        usr_cfg = self.usr_cfg_dir + "/" + self.ign_file
        if not os.path.isfile(usr_cfg):
            os.makedirs(self.usr_cfg_dir, exist_ok=True)
            orig_ign_file = os.path.join(
                self.rules_path,
                self.ign_file)
            # Get local copy from rules folder
            df_ign_file = os.path.join(self.rules_path, self.ign_file)
            if os.path.exists(df_ign_file):
                shutil.copyfile(df_ign_file, usr_cfg)
            else:
                self.debug.error('index file not found: ' + ignore_file)
        else:
            print('exist file')

    def parse_index(self):
        ignore_file = os.path.join(self.rules_path, self.ign_file)
        print(ignore_file)
        if os.path.exists(ignore_file):
            f = open(ignore_file)
            data = json.load(f)
            f.close()
            return data
        else:
            self.debug.error('index file not found: ' + ignore_file)

    # def load_ignore(self):
        #sdsd

    # def load_rule(self):
        #sdsd

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
        self.usr_cfg_dir = os.path.expanduser("~") + "/.config/thunderabsa/"
        self.create_cfg_folder()

    def merge_dicts(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def create_cfg_folder(self):
        if not os.path.exists(self.usr_cfg_dir):
            os.makedirs(self.usr_cfg_dir, exist_ok=True)

    def create_cfg_file(self, filename):
        cfg_file = self.usr_cfg_dir + "/" + filename
        if not os.path.isfile(cfg_file):
            rule_file = os.path.join(self.rules_path, filename)
            if os.path.exists(rule_file):
                shutil.copyfile(rule_file, cfg_file)
            else:
                self.debug.error('index file not found: ' + rule_file)
        return cfg_file

    def update_index(self, json_data):
        idx_path = self.create_cfg_file(self.idx_file)
        f = open(idx_path)
        data = json.load(f)
        f.close()
        idx_merge = self.merge_dicts(data, json_data)
        print(idx_merge)
        return idx_merge


    def load_index(self, json_data):
        self.create_cfg_file(self.idx_file)
        self.update_index(json_data)

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

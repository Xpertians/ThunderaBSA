import os
import re
import json
import hashlib
import os.path
from os import path
from . import ErrorHandler
import shutil
import configparser


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
        self.load_index()
        self.load_ignore()

    def get_ignore(self):
        return self.ignore

    def get_rules(self):
        return self.rules
        
    def file_checksum(self, file_path):
        with open(file_path, "rb") as f:
            file_hash = hashlib.md5()
            chunk = f.read(8192)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(8192)
        return file_hash.hexdigest()

    def merge_dicts(self, dict1, dict2):
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
                self.debug.error('rule file not found: ' + filename)
        return cfg_file

    def update_index(self, json_data):
        idx_path = self.create_cfg_file(self.idx_file)
        f = open(idx_path)
        data = json.load(f)
        f.close()
        idx_merge = self.merge_dicts(data, json_data)
        with open(idx_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(idx_merge, ensure_ascii=False))

    def load_index(self):
        cfg_file = self.create_cfg_file(self.idx_file)
        if os.path.isfile(cfg_file):
            f = open(cfg_file)
            idx_dict = json.load(f)
            f.close()
            for key, value in idx_dict.items():
                if bool(value['active']):
                    rule_file = self.create_cfg_file(value['filename'])
                    checksum = self.file_checksum(rule_file)
                    if key == checksum:
                        f = open(rule_file)
                        rule_dict = json.load(f)
                        f.close()
                        self.rules[key] = rule_dict
                    else:
                        self.debug.error(
                            'rule cfg checksum not match for file '
                            + value['filename'])
                        print(checksum)
        else:
            self.debug.error('index cfg file not found: ' + cfg_file)

    def load_ignore(self):
        cfg_file = self.create_cfg_file(self.ign_file)
        if os.path.isfile(cfg_file):
            f = open(cfg_file)
            ign_dict = json.load(f)
            f.close()
            for key, value in ign_dict.items():
                self.ignore = value
        else:
            self.debug.error('index cfg file not found: ' + cfg_file)

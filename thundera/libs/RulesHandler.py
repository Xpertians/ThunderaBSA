import os
import re
import json
import hashlib
import os.path
from os import path
from . import ErrorHandler
import shutil
import configparser
from pkg_resources import resource_stream


class RulesHandler:

    def __init__(self, errorHandler):
        self.debug = errorHandler
        self.ignore = []
        self.rules = {}
        self.ign_file = "default_ignore.json"
        self.idx_file = "default_index.json"
        self.load_index()
        self.load_ignore()

    def get_ignore(self):
        return self.ignore

    def get_rules(self):
        return self.rules

    def merge_dicts(self, dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def load_index(self):
        idx_file = resource_stream('thundera', 'rules/'+self.idx_file)
        idx_dict = json.load(idx_file)
        for key, value in idx_dict.items():
            if bool(value['active']):
                rule_file = resource_stream('thundera', 'rules/'+value['filename'])
                rule_dict = json.load(rule_file)
                self.rules[key] = rule_dict

    def load_ignore(self):
        cfg_file = resource_stream('thundera', 'rules/'+self.ign_file)
        ign_dict = json.load(cfg_file)
        for key, value in ign_dict.items():
            self.ignore = value

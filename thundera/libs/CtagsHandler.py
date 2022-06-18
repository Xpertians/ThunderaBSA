import subprocess
import re
from . import CtagsCmdFactory


class CtagsHandler:

    def __init__(self, target):
        self.target = target
        self.cmd = CtagsCmdFactory.CtagsCmdFactory(target)
        self.symlst = []

    def setLang(self, langName):
        self.cmd.setLang(langName)

    def setLangMap(self, langMap):
        self.cmd.setLangMap(langMap)

    def setOption(self, cmdOpt):
        self.cmd.setOption(cmdOpt)

    def run(self):
        cmd = self.cmd.buildCmd()
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (result, error) = process.communicate()
        rc = process.wait()
        process.stdout.close()
        for line in result.splitlines():
            cols = line.split()
            if len(cols) >= 2:
                if len(cols[0]) >= 5:
                    symstr = str(cols[0])
                    if "b'" in symstr:
                        m = re.compile(r"b'(.*?)'").search(symstr)
                        symstr = m.group(1)
                    self.symlst.append(symstr)
        self.symlst = sorted(set(self.symlst))
        return ','.join(self.symlst)

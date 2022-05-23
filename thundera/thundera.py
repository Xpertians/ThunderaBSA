#!/usr/bin/env python3
import os
import sys
import click
import calendar
import time
import terminal_banner
from shutil import which
from pathlib import Path
from thundera.libs import ErrorHandler
from . import Scanner

os.environ['LANG'] = 'C.UTF-8'
os.environ['LC_ALL'] = 'C.UTF-8'

debug = ErrorHandler.ErrorHandler(__name__)
filelist = []


@click.command()
@click.argument(
    'target',
    type=click.Path(exists=True)
)
@click.option('--scan/--no-scan', default=False)
def cli(target, scan):

    rv = sys.platform
    if scan:
        rv = rv.upper() + '!!!!111'
    click.echo(rv)

    """ Thundera BSA """
    banner_txt = "Thundera Binary Static Analysis (BSA)"
    banner_obj = terminal_banner.Banner(banner_txt)
    print(banner_obj)
    print('')

    cmdlist = ["ctags", "readelf", "exiftool", "strings"]
    for cmd in cmdlist:
        if which(cmd) is None:
            eMSG = "Thundera requires "+cmd+" to run"
            debug.error(eMSG)
            eMSG = "Please install to continue..."
            debug.error(eMSG)
            exit()

    if os.name == "posix":
        if target.endswith('/'):
            target = target[:-1]
        if os.path.isdir(target):
            eMSG = "Scanning the folder "+target
            print(eMSG)
            paths = [
                os.path.join(target, fn)
                for fn in next(os.walk(target))[2]]
            filelist.extend(paths)
            Scanner.Scanner(debug, filelist)
        elif os.path.isfile(target):
            eMSG = "Scanning the file "+target
            print(eMSG)
            filelist.append(target)
            Scanner.Scanner(debug, filelist)
        else:
            debug.info('*** Target Path: %s' % target)
            debug.info('*** Working Directory: %s' % workdir)
            eMSG = "The target " + target
            eMSG = eMSG + " it\'s a special file (socket, FIFO, device file)"
            debug.error(eMSG)
            print(eMSG)
            print('')
    else:
        eMSG = "Thundera BSA only supports POSIX based OS"
        debug.error(eMSG)
        print(eMSG)
        print('')


if __name__ == '__main__':
    cli()

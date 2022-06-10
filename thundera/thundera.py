#!/usr/bin/env python3
import os
import sys
import click
import calendar
import time
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
@click.option(
    '--extract',
    is_flag=True,
    show_default=True,
    default=False,
    help='Extract Symbols ONLY')
@click.option(
    '--filter',
    'filter',
    show_default=False,
    help='Rules filter string')
@click.option(
    '--update',
    is_flag=True,
    show_default=False,
    default=False,
    help='Update Compliance Library (CL)')
@click.option(
    '--output',
    default='report.json',
    show_default=False,
    help='Report file name')
@click.option('--format',
              type=click.Choice(['JSON', 'CSV'], case_sensitive=False))
def cli(target, extract, filter, update, output, format):

    """ Thundera BSA """
    print('*'*44)
    print("* Thundera <> Binary Static Analysis (BSA) *")
    print('*'*44)
    print('')

    if filter:
        filter_str = str(filter)
    else:
        filter_str = ''

    if format:
        if format.upper() == 'CSV':
            format = 'CSV'
        else:
            format = 'JSON'
    else:
        format = 'JSON'
        
    if update:
        msg = "function UPDATE not available"
        click.echo(msg)
        print('ERR:', msg)
        exit()

    cmdlist = ["ctags", "readelf", "exiftool"]
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
            eMSG = "Scanning folder "+target
            print(eMSG)
            for cdp, csb, cfs in os.walk(target):
                for aFile in cfs:
                    file_path = str(os.path.join(cdp, aFile))
                    filelist.append(file_path)
            Scanner.Scanner(debug, extract, filter_str, format, filelist)
        elif os.path.isfile(target):
            eMSG = "Scanning file "+target
            print(eMSG)
            filelist.append(target)
            Scanner.Scanner(debug, extract, filter_str, format, filelist)
        else:
            debug.info('*** Target Path: %s' % target)
            debug.info('*** Working Directory: %s' % workdir)
            eMSG = "The target " + target
            eMSG = eMSG + " it\'s a special file (socket, FIFO, device file)"
            debug.error(eMSG)
            print(eMSG)
            print('')
    else:
        eMSG = "ThunderaBSA only supports POSIX based OS"
        debug.error(eMSG)
        print(eMSG)
        print('')


if __name__ == '__main__':
    cli()

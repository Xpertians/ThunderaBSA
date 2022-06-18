# ThunderaBSA-Cli

ThunderaBSA it's a Binary Static Analysis tool that uses symbols (strings) extracted from a binary (compiled) software to "infer" the list of Open Source packages used in the software.

ThunderaBSA doesn't perform reverse engineering over the software. Instead, it extracts the symbols (strings) from software in the same fashion as the operative system scan for file mime-types or file sizes.

## Context

A "symbol" it's a representation of a file property (file name, file path, folders names) or content (symtree, class names, function names, variable names).

ThunderaBSA extract the symbols from the source code of well known OSS packages to build a Compliance Library (CL), that's later used to match symbols on binary files.

## Installation
ThunderaBSA requires a few tools to be available on your system:

$ sudo apt install python3-pip

$ sudo apt install universal-ctags elfutils binutils libimage-exiftool-perl g++ pycodestyle

$ pip3 install thunderabsa

** If you are not able to find universal-ctags, please install the package from source. This tool will not work with the Ubuntu package exuberant-ctags. **

## Development
### Libraries
pip3 install twine setuptools wheel pycodestyle pyinstaller virtualenv


elif filetype in 'application/gzip':
    print('gzip:', file)
    if os.path.isdir(new_dir):
        shutil.rmtree(new_dir)
    if os.path.isfile(new_dir):
        new_dir = new_dir + '_tmp'
    os.mkdir(new_dir)
    print('new_dir:', new_dir)
    new_base = os.path.basename(file).replace(".gz", "")
    new_file = os.path.join(new_dir, new_base)
    print('newfile:', new_file)
    if os.path.isfile(new_file):
        os.remove(new_file)
    #with gzip.open(file, 'rb') as f_in:
    #    with open(new_file, 'wb') as f_out:
    #        shutil.copyfileobj(f_in, f_out)
    self.filelist.append(new_file)
    if file in self.filelist:
        self.filelist.remove(file)
    else:
        self.debug.error(" file not listed:" + file)


application/zlib
text/x-lisp

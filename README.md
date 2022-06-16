# ThunderaBSA-Cli

ThunderaBSA it's a Binary Static Analysis tool that infers what Open Source packages are present on binary apps by searching for "symbols."

A "symbol" for ThunderaBSA it's the representation of a file property (file name, file path, folders names) or content (symtree, class names, function names, variable names).

ThunderaBSA doesn't perform reverse engineering over the software. Instead, it extracts the symbols offered by the file's metadata, the same way as the operative system scan for file mime-types or file sizes.

The CLI (ThunderaBSA CLI) it's one of the three main components of the project. The CLI tool scan files to extract symbols and export the "symbols" to a report file. The reports can be used later by other components to perform the symbol matching offline.

## Installation
ThunderaBSA requires a few tools to be available on your system:

$ sudo apt install python3-pip

$ sudo apt install universal-ctags elfutils binutils libimage-exiftool-perl g++ pycodestyle

$ pip3 install thunderabsa

If you are not able to find universal-ctags, please install the package from source. This tool will not work with the Ubuntu package exuberant-ctags, you need to install universal-ctags

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

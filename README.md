# ThunderaBSA

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

**If you are not able to find universal-ctags, please install the package from source. This tool will not work with the Ubuntu package exuberant-ctags.**

## Using Thundera

After installing ThunderaBSA, the options to run the software are simple:

$ thundera folder/

If you prefer to obtain a CSV report instead of JSON, use the option --output:

$ thundera folder/ --output CSV

### Rules generation

ThunderaBSA can extract symbols from any software by using the function **extract**.

$ thundera --extract folder/

The tool will generate a single JSON file with the list of symbols. In some cases, the output can be optimized by filtering an string.

$ thundera --extract folder/ --filter filter-string

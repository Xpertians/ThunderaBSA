#!/bin/bash
if [ ! -d "logs" ]; then
  mkdir logs
fi

echo "Removing old Thundera WHL"
pip3 uninstall thunderabsa -y > logs/pip3uninstall.log

echo "Checking PEP8"
python3 -m pycodestyle --exclude='*testfiles*' . | grep -v 'build' | grep -v 'dist' | grep -v 'W605'> logs/pep8.log

echo "Creating Thundera ENV"
python3 -m venv thundera_env > logs/virtualenv.log

echo "Activating Thundera ENV"
activate="thundera_env/bin/activate"
if [ ! -f "$activate" ]
then
    echo "ERROR: activate not found at $activate"
    return 1
fi
. "$activate"

echo "Installing old Thundera WHL"
python3 setup.py install > logs/pip3install.log

echo "Running Thundera WHL"
#thundera --extract ./testfiles/folder.zip
#rm -rf ./testfiles/folder/
#thundera ./testfiles/KeplerPackage_linux_0.2_11-May-2022_1652283758.tar.gz
#rm -rf ./testfiles/KeplerPackage_linux_0.2_11-May-2022_1652283758.tarrm -rf ./testfiles/KeplerPackage_linux_0.2_11-May-2022_1652283758.tar
thundera --extract ./testfiles/Prog.cpp
#thundera --extract ./testfiles/Prog.cpp
#thundera --extract ./testfiles/Prog.cpp
#thundera ./testfiles/testfolder/
#thundera /bin/
#thundera ./testfiles/packages/avro-master/
#thundera ./testfiles/


echo "Deactivating Thundera ENV"
deactivate
echo "Deleting Thundera ENV"
rm -rf thundera_env/

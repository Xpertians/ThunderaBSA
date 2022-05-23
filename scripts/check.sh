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
# thundera ./testfiles/libgcc_s.so.1 --scan
# thundera ./testfiles/libgcc_s.so.1 --no-scan
thundera /bin/

echo "Deactivating Thundera ENV"
deactivate
echo "Deleting Thundera ENV"
rm -rf thundera_env/

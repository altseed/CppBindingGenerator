#!/bin/sh

cd `dirname $0`
cd ..
export PYTHONPATH=`pwd`

python3 tests/csharp.py
python3 tests/rust.py
python3 tests/cplusplus.py
./tests/scripts/GenerateProjects_Mac.sh

#!/bin/sh

cd `dirname $0`/..
export PYTHONPATH=`pwd`

python3 tests/csharp.py
python3 tests/rust.py
python3 tests/cplusplus.py
./scripts/GenerateProjects_Mac.sh

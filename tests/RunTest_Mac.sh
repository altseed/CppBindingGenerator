#!/bin/sh

cd `dirname $0`/..
export PYTHONPATH=`pwd`

python3 tests/csharp.py
python3 tests/cplusplus.py
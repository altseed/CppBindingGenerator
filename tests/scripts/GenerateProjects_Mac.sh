#!/bin/sh
cd `dirname $0`
cd ../results
mkdir Build
cd Build
cmake -G "Xcode" ../

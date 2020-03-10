#!/bin/sh
cd `dirname $0`
cp ../../build/DEBUG/libCommon.dylib ./target/debug/.
cp ../../build/RELEASE/libCommon.dylib ./target/release/.
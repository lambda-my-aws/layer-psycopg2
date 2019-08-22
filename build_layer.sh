#!/usr/bin/env bash

LAYER_NAME=$1

PY_VERSION=`python --version | head -1 | tr -cd [0-9.]`
PY_VERSION=`echo $PY_VERSION | awk -F. '{print "python"$1"."$2}'`
PY_BUILD=$PWD/build/python/lib/${PY_VERSION}/site-packages/${LAYER_NAME}

mkdir -p $PY_BUILD

pip install -t $PY_BUILD -r requirements.txt
find $PWD -type d -name "__pycache__" -exec rm -rf {} +
cd build; zip -r9 ../layer.zip * ; cd ..
rm -rf build

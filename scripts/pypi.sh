#!/bin/bash

if [ ! -e dist ]
then
    rm -rf dist
fi

python -m build
twine upload dist/*


#!/bin/bash

echo Working directory: ${pwd}

if [ -d "prof" ]
then
    rm -rf prof
fi

if [ -e "docs/_build/combined.svg" ]
then
    rm docs/_build/combined.svg
fi

python -m pytest \
    --profile-svg \
    -o log_cli=true \
    -k pickl \
    -vv

mv prof/combined.svg docs/_build/

echo Done!


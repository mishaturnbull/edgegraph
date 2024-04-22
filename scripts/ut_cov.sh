#!/bin/bash

echo Working directory: ${pwd}

if [ ! -e .coverage ]
then
   rm .coverage
fi

if [ -d "docs/_build/htmlcov" ]
then
   rm -rf docs/_build/htmlcov
fi

pytest --cov=edgegraph \
    --cov-branch \
    --cov-fail-under=100

coverage html
mv htmlcov docs/_build/

echo Done!

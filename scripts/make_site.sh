#!/bin/bash

mkdir -p site

uv run scripts/make_home.py > site/index.html
prettier -w site/index.html

ln -rs ./assets ./site/
ln -rs ./style ./site/
ln -rs ./sources/js ./site/

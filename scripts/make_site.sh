#!/bin/bash

mkdir -p site

# uv run scripts/make_all.py
uv run scripts/make_home.py > site/index.html
# uv run scripts/make_products.py > site/
prettier -w site/index.html

ln -rs ./assets ./site/
ln -rs ./style ./site/
ln -rs ./sources/js ./site/

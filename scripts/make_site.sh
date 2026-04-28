#!/bin/bash

mkdir -p site

uv run scripts/make_home.py > site/index.html
prettier -w site/index.html

ln -s ./assets ./site/

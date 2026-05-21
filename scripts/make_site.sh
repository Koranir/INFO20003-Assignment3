#!/bin/bash

mkdir -p site
mkdir -p site/products
mkdir -p site/authors
mkdir -p site/data

uv run scripts/make_home.py >site/index.html
uv run scripts/make_products.py
uv run scripts/make_titles.py >site/titles.html
uv run scripts/make_authors.py >site/authors.html
uv run scripts/make_author_profiles.py
uv run scripts/make_cart.py >site/cart.html
uv run scripts/make_cart_products.py >site/data/cart-products.json
uv run scripts/make_order_confirmation.py >site/order-confirmation.html

prettier -w site/index.html
prettier -w site/products/*.html
prettier -w site/titles.html
prettier -w site/authors.html
prettier -w site/authors/*.html
prettier -w site/data/*.json

ln -rsfn ./assets ./site/assets
ln -rsfn ./style ./site/style
ln -rsfn ./sources/js ./site/js

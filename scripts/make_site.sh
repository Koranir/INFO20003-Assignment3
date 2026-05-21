#!/bin/bash

mkdir -p site
mkdir -p site/products

uv run scripts/make_home.py >site/index.html
uv run scripts/make_products.py
uv run scripts/make_cart.py >site/cart.html
uv run scripts/make_order_confirmation.py >site/order-confirmation.html

prettier -w site/index.html
prettier -w site/products/*.html

ln -rs ./assets ./site/
ln -rs ./style ./site/
ln -rs ./sources/js ./site/

import yaml
from make_product import make_product

products = yaml.full_load(open("sources/books.yaml"))

for key, product in products.items():
    writer = open(f"site/products/{key}.html", "w")
    writer.write(str(make_product(product)))

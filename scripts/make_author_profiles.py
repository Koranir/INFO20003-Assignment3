import os

import yaml
from make_authors import make_author_page


authors = yaml.full_load(open("sources/authors.yaml", "r"))
books = yaml.full_load(open("sources/books.yaml", "r"))

os.makedirs("site/authors", exist_ok=True)

for key, author in authors.items():
    with open(f"site/authors/{key}.html", "w") as writer:
        writer.write(str(make_author_page(key, author, books)))

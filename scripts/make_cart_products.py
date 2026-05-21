import json

import yaml

books = yaml.full_load(open("sources/books.yaml", "r"))
cart_books = {
    key: {
        "title": book["title"],
        "author": book["author"],
        "price": book["price"],
    }
    for key, book in books.items()
}

print(json.dumps(cart_books))

import dominate.tags as d
import yaml
from paths import cover_path, product_page_path


def make_bestsellers():
    books = yaml.full_load(open("sources/books.yaml", "r"))
    bestsellers = yaml.full_load(open("sources/bestsellers.yaml", "r"))

    for key in bestsellers:
        book = books[key]

        with d.a(cls="bestseller", href=product_page_path(key)):
            d.img(
                src=cover_path(key),
                alt=f"Cover of {book['title']}",
            )
            with d.div(cls="bestseller-details"):
                d.h3(book["title"])
                d.address(book["author"])

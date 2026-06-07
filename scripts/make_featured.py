from os.path import exists

import dominate.tags as d
import yaml
from paths import cover_path, portrait_fs_path, portrait_path, product_page_path


@d.section
def make_featured(key, book):
    with d.div(cls="images"):
        if exists(portrait_fs_path(book["author"])):
            with d.img(cls="author-portrait"):
                d.attr(
                    src=portrait_path(book["author"]),
                    alt=f"Portrait of {book['author']}",
                )
        with d.img(cls="cover"):
            d.attr(
                src=cover_path(key),
                alt=f"Cover of {book['title']}",
            )
    with d.div(cls="details"):
        with d.div(cls="details-text"):
            d.h3(book["title"])
            d.address(book["author"])

            d.p(book["short_description"])
        d.a("Read more »", cls="bold", href=product_page_path(key))


def make_all_featured():
    featured = yaml.full_load(open("sources/featured.yaml", "r"))
    books = yaml.full_load(open("sources/books.yaml", "r"))

    # print(featured, books)

    [make_featured(book, books[book]) for book in featured]


if __name__ == "__main__":
    make_all_featured()

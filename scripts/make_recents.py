import dominate.tags as d
import yaml
from paths import cover_path, product_page_path


def make_recents():
    books = yaml.full_load(open("sources/books.yaml", "r"))
    recents = yaml.full_load(open("sources/recents.yaml", "r"))

    with d.div(cls="recent-wheel"):
        for key, book in [(key, books[key]) for key in recents]:
            d.button(book["title"], cls="recent-title")

    for key, book in [(key, books[key]) for key in recents]:
        d.img(
            cls="recent-cover",
            src=cover_path(key),
            alt=f"Cover of {book['title']}",
        )

        with d.div(cls="recent-description"):
            d.p(book["short_description"])
            d.a("Read more »", cls="bold", href=product_page_path(key))

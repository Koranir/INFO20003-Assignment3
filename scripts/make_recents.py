import dominate.tags as d
import yaml
from paths import cover_path, product_page_path


def make_recents():
    books = yaml.full_load(open("sources/books.yaml", "r"))
    recents = yaml.full_load(open("sources/recents.yaml", "r"))

    with d.div(cls="recents-left"):
        first = True
        for key, book in [(key, books[key]) for key in recents]:
            with d.img(
                cls="recent-cover",
                src=cover_path(key),
                alt=f"Cover of {book['title']}",
                id=f"recent-cover-{key}",
            ) as img:
                if not first:
                    img.set_attribute("hidden", "")
                first = False

    with d.div(cls="recents-right"):
        with d.section(cls="recent-wheel"):
            first = True
            for key, book in [(key, books[key]) for key in recents]:
                with d.button(
                    book["title"],
                    cls="recent-title",
                    id=f"recent-title-{key}",
                    type="button",
                ) as but:
                    if first:
                        but.set_attribute("x-checked", "true")
                    but.set_attribute("aria-pressed", str(first).lower())
                    first = False

        with d.div(cls="recent-descriptions"):
            first = True
            for key, book in [(key, books[key]) for key in recents]:
                with d.section(
                    cls="recent-description",
                    id=f"recent-description-{key}",
                ) as sect:
                    d.p(book["short_description"])
                    d.a(
                        "Read more »",
                        cls="bold",
                        href=product_page_path(key),
                    )
                    if not first:
                        sect.set_attribute("hidden", "")
                    first = False

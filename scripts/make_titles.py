import dominate.tags as d
import yaml
from make_doc import make_doc
from make_footer import make_footer
from make_header import make_header
from paths import asset_path, cover_path, page_path, product_page_path


def sorted_books(books):
    return sorted(books.items(), key=lambda item: item[1]["title"].lower())


doc = make_doc("Titles")
books = yaml.full_load(open("sources/books.yaml", "r"))

with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main(cls="repository-page"):
            with d.div(cls="repository-header"):
                d.h2(
                    "Titles",
                    cls="section-title",
                    style=f"--styled-asset-path: url('{asset_path('titles.svg')}')",
                )

            with d.section(cls="repository-toolbar"):
                d.p(f"{len(books)} titles")
                d.a("Browse authors", href=page_path("authors.html"), cls="bold")

            with d.div(cls="title-repository"):
                for key, book in sorted_books(books):
                    with d.article(cls="repository-card title-card"):
                        d.a(
                            d.img(
                                src=cover_path(key),
                                alt=f"Cover of {book['title']}",
                            ),
                            href=product_page_path(key),
                            cls="repository-cover-link",
                        )
                        with d.div(cls="repository-card-details"):
                            d.h3(book["title"])
                            d.address(book["author"])
                            with d.dl(cls="repository-meta"):
                                with d.div(cls="repository-meta-row"):
                                    d.dt("Released")
                                    d.dd(book["release_date"])
                                with d.div(cls="repository-meta-row"):
                                    d.dt("Price")
                                    d.dd(f"A$ {book['price']}")
                            d.a(
                                "View title »",
                                href=product_page_path(key),
                                cls="bold",
                            )

    make_footer()

print(doc)

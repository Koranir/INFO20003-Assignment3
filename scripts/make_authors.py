from os.path import exists

import dominate.tags as d
import yaml
from make_doc import make_doc
from make_footer import make_footer
from make_header import make_header
from paths import cover_path, portrait_path, product_page_path


def sorted_authors(authors):
    return sorted(authors.items(), key=lambda item: item[1]["sort_name"].lower())


def make_author_page(author_key, author, books):
    doc = make_doc(author["name"])
    author_books = [(key, books[key]) for key in author["books"] if key in books]

    with doc.body:
        with d.div(cls="content-area"):
            make_header()

            with d.main(cls="author-page"):
                with d.div(cls="repository-header"):
                    d.h2(author["name"], cls="section-title")

                with d.section(cls="author-profile"):
                    if exists(f".{portrait_path(author['name'])}"):
                        d.img(
                            src=portrait_path(author["name"]),
                            alt=f"Portrait of {author['name']}",
                            cls="author-profile-portrait",
                        )
                    with d.div(cls="author-profile-copy"):
                        d.h3("About the Author")
                        for line in author["long_description"].split("\n"):
                            d.p(line)

                with d.section(cls="author-bibliography"):
                    d.h3("Titles")
                    with d.div(cls="bibliography-list"):
                        for book_key, book in author_books:
                            with d.a(
                                href=product_page_path(book_key),
                                cls="bibliography-item",
                            ):
                                d.img(
                                    src=cover_path(book_key),
                                    alt=f"Cover of {book['title']}",
                                )
                                with d.div():
                                    d.h3(book["title"])
                                    d.p(book["release_date"])

        make_footer()
    return doc


def make_author_index(authors, books):
    doc = make_doc("Authors")

    with doc.body:
        with d.div(cls="content-area"):
            make_header()

            with d.main(cls="repository-page"):
                with d.div(cls="repository-header"):
                    d.h2(
                        "Authors",
                        cls="section-title",
                        style="--styled-asset-path: url('/assets/authors.svg')",
                    )

                with d.section(cls="repository-toolbar"):
                    d.p(f"{len(authors)} authors")
                    d.a("Browse titles", href="/titles.html", cls="bold")

                with d.div(cls="author-repository"):
                    current_letter = None
                    for key, author in sorted_authors(authors):
                        letter = author["sort_name"][0].upper()
                        if letter != current_letter:
                            current_letter = letter
                            d.h3(letter, cls="repository-letter")

                        with d.article(cls="repository-card author-card"):
                            with d.div(cls="author-card-heading"):
                                d.h3(author["name"])
                                title_count = len(author["books"])
                                title_label = "title" if title_count == 1 else "titles"
                                d.p(f"{title_count} {title_label}")
                            d.p(author["short_description"])
                            with d.ul(cls="compact-title-list"):
                                for book_key in author["books"]:
                                    if book_key not in books:
                                        continue
                                    d.li(
                                        d.a(
                                            books[book_key]["title"],
                                            href=product_page_path(book_key),
                                        )
                                    )
                            d.a(
                                "View profile »",
                                href=f"/authors/{key}.html",
                                cls="bold",
                            )

        make_footer()
    return doc


if __name__ == "__main__":
    authors = yaml.full_load(open("sources/authors.yaml", "r"))
    books = yaml.full_load(open("sources/books.yaml", "r"))

    print(make_author_index(authors, books))

import json

import dominate
import dominate.tags as d
import yaml
from make_doc import make_doc
from make_footer import make_footer
from make_header import make_header
from make_section_title import make_section_title
from paths import author_page_path, cover_path, page_path

authors = yaml.full_load(open("sources/authors.yaml", "r"))


def make_product(key, product):
    doc = make_doc(product["title"], depth=1)
    with doc.body:
        with d.div(cls="content-area"):
            make_header()

            with d.main(cls="product-page"):
                with d.div(cls="product-header"):
                    make_section_title(product["title"], f"headers/{key}.svg")
                    d.h3(product["author"], cls="section-subtitle")

                d.img(
                    src=cover_path(key),
                    alt=f"Cover of {product['title']}",
                    cls="product-cover-mobile",
                )

                with d.section(cls="product-description"):
                    d.img(
                        src=cover_path(key),
                        alt=f"Cover of {product['title']}",
                        cls="product-cover",
                    )

                    d.h3("Description")
                    for line in product["long_description"].split("\n"):
                        d.p(line)

                with d.details(cls="product-description-mobile", open=""):
                    d.summary("Description")
                    for line in product["long_description"].split("\n"):
                        d.p(line)

                with d.div(cls="product-sidebar"):
                    cart_details = json.dumps(
                        {
                            "title": product["title"],
                            "author": product["author"],
                            "price": product["price"],
                        }
                    )
                    with d.button(
                        cls="purchase bold",
                        onclick=f"addToCart('{key}', 1, {cart_details})",
                    ):
                        d.span(f"A$ {product['price']}", cls="price")
                        d.span("Add to Cart")
                        dominate.util.raw(
                            """
                        <svg width="15" height="16" viewBox="0 0 15 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g clip-path="url(#clip0_12_8270)">
                        <path d="M0.625 0.666504H3.125L4.8 9.59317C4.85715 9.9001 5.01369 10.1758 5.24222 10.372C5.47074 10.5683 5.75669 10.6725 6.05 10.6665H12.125C12.4183 10.6725 12.7043 10.5683 12.9328 10.372C13.1613 10.1758 13.3178 9.9001 13.375 9.59317L14.375 3.99984H3.75M6.25 13.9998C6.25 14.368 5.97018 14.6665 5.625 14.6665C5.27982 14.6665 5 14.368 5 13.9998C5 13.6316 5.27982 13.3332 5.625 13.3332C5.97018 13.3332 6.25 13.6316 6.25 13.9998ZM13.125 13.9998C13.125 14.368 12.8452 14.6665 12.5 14.6665C12.1548 14.6665 11.875 14.368 11.875 13.9998C11.875 13.6316 12.1548 13.3332 12.5 13.3332C12.8452 13.3332 13.125 13.6316 13.125 13.9998Z" stroke="#DCCEBD" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                        </g>
                        <defs>
                        <clipPath id="clip0_12_8270">
                        <rect width="15" height="16" fill="white"/>
                        </clipPath>
                        </defs>
                        </svg>
                        """
                        )
                    d.a(
                        "Download Sample »",
                        href=page_path(f"samples/{key}.pdf"),
                        cls="bold",
                    )
                    d.a(
                        "Download Cover »",
                        href=cover_path(key),
                        cls="bold",
                    )

                with d.div(cls="product-information"):
                    with d.details(open=""):
                        d.summary("Information")
                        with d.table():
                            with d.tbody():
                                with d.tr():
                                    d.td("ISBN")
                                    d.td(product["isbn"])
                                with d.tr():
                                    d.td("Release")
                                    d.td(product["release_date"])
                                with d.tr():
                                    d.td("Pages")
                                    d.td(str(product["page_count"]))
                    with d.details(open=""):
                        d.summary("About the Author")

                        with d.div(cls="author-infos"):
                            # Split author by ', ' and ' and ' to get individual author names, then replace spaces with dashes and lowercase for the URLs
                            for author in product["author"].split(", "):
                                for sub_author in author.split(" and "):
                                    author_key = sub_author.replace(" ", "-").lower()
                                    d.p(authors[author_key]["short_description"])
                                    d.a(
                                        "Go to Profile »",
                                        href=author_page_path(author_key),
                                        cls="bold",
                                    )

                if not len(product["reviews"]) == 0:
                    with d.div(cls="product-reviews"):
                        make_section_title("Reviews", "reviews.svg")

                        for review in product["reviews"]:
                            with d.details(cls="review"):
                                d.summary(f"{review['title']}")
                                d.p(review["text"])

        make_footer()
    return doc

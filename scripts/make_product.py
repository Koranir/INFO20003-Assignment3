import dominate
import dominate.tags as d
import yaml
from make_doc import make_doc
from make_footer import make_footer
from make_header import make_header

authors = yaml.full_load(open("sources/authors.yaml", "r"))


def make_product(key, product):
    doc = make_doc(product["title"])
    with doc.body:
        with d.div(cls="content-area"):
            make_header()

            with d.main(cls="product-page"):
                with d.div(cls="product-header"):
                    d.h2(
                        product["title"],
                        cls="section-title",
                        style=f"--styled-asset-path: url('/assets/headers/{key}.svg')",
                    )
                    d.h3(product["author"], cls="section-subtitle")

                d.img(
                    src=f"/assets/books/{key}/cover.jpg",
                    alt=f"Cover of {product['title']}",
                    cls="product-cover-mobile",
                )

                with d.section(cls="product-description"):
                    d.img(
                        src=f"/assets/books/{key}/cover.jpg",
                        alt=f"Cover of {product['title']}",
                        cls="product-cover",
                    )

                    d.h3("Description")
                    for line in product["long_description"].split("\n"):
                        d.p(line)

                with d.div(cls="product-sidebar"):
                    with d.button(cls="purchase bold"):
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
                    d.a("Download Sample »", href=f"/samples/{key}.pdf", cls="bold")
                    d.a(
                        "Download Cover »",
                        href=f"/assets/books/{key}/cover.jpg",
                        cls="bold",
                    )

                with d.div(cls="product-information"):
                    with d.section():
                        d.h3("Information")
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
                    with d.section():
                        # Split author by ', ' and ' and ' to get individual author names, then replace spaces with dashes and lowercase for the URLs
                        for author in product["author"].split(", "):
                            for sub_author in author.split(" and "):
                                author_key = sub_author.replace(" ", "-").lower()
                                d.h3("About the Author")
                                d.p(authors[author_key]["short_description"])
                                d.a(
                                    "Go to Profile »",
                                    href=f"/authors/{author_key}.html",
                                    cls="bold",
                                )

                if not len(product["reviews"]) == 0:
                    with d.div(cls="product-reviews"):
                        d.h2(
                            "Reviews",
                            cls="section-title",
                            style="--styled-asset-path: url('/assets/reviews.svg')",
                        )

                        for review in product["reviews"]:
                            with d.details(cls="review"):
                                d.summary(f"{review['title']}")
                                d.p(review["text"])

        make_footer()
    return doc

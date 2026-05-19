import dominate
import dominate.tags as d
from make_bestsellers import make_bestsellers
from make_featured import make_all_featured
from make_header import make_header
from make_recents import make_recents

doc = dominate.document(title="Black Pepper Publishing - Home")
with doc.head:
    d.meta(charset="UTF-8")
    d.meta(name="viewport", content="width=device-width, initial-scale=1.0")
    d.link(rel="stylesheet", href="/style/index.css")

    # <link rel="preconnect" href="https://fonts.googleapis.com">
    # <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    # <link href="https://fonts.googleapis.com/css2?family=Crimson+Text&display=swap" rel="stylesheet">

    d.link(rel="preconnect", href="https://fonts.googleapis.com")
    d.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True)
    d.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@1,600&family=Crimson+Text:wght@400;600&family=Roboto&display=swap",
    )
    d.script(src="/js/cart.js")

with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main():
            with d.article():
                d.h2(
                    "Featured",
                    cls="section-title",
                    style="--styled-asset-path: url('/assets/featured.svg')",
                )

                with d.div(cls="featured"):
                    make_all_featured()

            with d.div(cls="content-with-sidebar"):
                with d.article():
                    d.h2(
                        "Recent Releases",
                        cls="section-title",
                        style="--styled-asset-path: url('/assets/recent-releases.svg')",
                    )

                    with d.div(cls="recent-releases"):
                        make_recents()
                with d.article(cls="sidebar"):
                    d.h2(
                        "Bestsellers",
                        cls="section-title",
                        style="--styled-asset-path: url('/assets/bestsellers.svg')",
                    )

                    with d.div(cls="bestsellers"):
                        make_bestsellers()

print(doc)

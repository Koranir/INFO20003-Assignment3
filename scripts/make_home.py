import dominate.tags as d
from make_bestsellers import make_bestsellers
from make_doc import make_doc
from make_featured import make_all_featured
from make_footer import make_footer
from make_header import make_header
from make_recents import make_recents

doc = make_doc("Home")
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

        make_footer()

print(doc)

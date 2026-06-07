import dominate.tags as d
from make_bestsellers import make_bestsellers
from make_doc import make_doc
from make_featured import make_all_featured
from make_footer import make_footer
from make_header import make_header
from make_recents import make_recents
from make_section_title import make_section_title

doc = make_doc("Home")
with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main():
            with d.article():
                make_section_title("Featured", "featured.svg")

                with d.div(cls="featured"):
                    make_all_featured()

            with d.div(cls="content-with-sidebar"):
                with d.article(cls="recent-releases"):
                    make_section_title("Recent Releases", "recent-releases.svg")

                    with d.div(cls="recents"):
                        make_recents()
                with d.section(cls="sidebar"):
                    make_section_title("Bestsellers", "bestsellers.svg")

                    with d.div(cls="bestsellers"):
                        make_bestsellers()

    make_footer()

print(doc)

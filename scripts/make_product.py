import dominate.tags as d
import yaml
from make_doc import make_doc
from make_footer import make_footer
from make_header import make_header


def make_product(key, product):
    doc = make_doc(product["title"])
    with doc.body:
        with d.div(cls="content-area"):
            make_header()

            with d.main():
                with d.article():
                    d.h2(
                        "Featured",
                        cls="section-title",
                        style=f"--styled-asset-path: url('/assets/headers/{key}.svg')",
                    )

                with d.div(cls="content-with-sidebar"):
                    pass

            make_footer()
    return doc

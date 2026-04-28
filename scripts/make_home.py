import dominate
import dominate.tags as d
from make_featured import make_all_featured
from make_header import make_header

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
        href="https://fonts.googleapis.com/css2?family=Crimson+Text&display=swap",
    )

with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main():
            with d.div(cls="featured"):
                make_all_featured()

print(doc)

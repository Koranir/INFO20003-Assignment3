import dominate
import dominate.tags as d
from make_featured import make_all_featured
from make_header import make_header

doc = dominate.document(title="Black Pepper Publishing - Home")
with doc.head:
    d.meta(charset="UTF-8")
    d.meta(name="viewport", content="width=device-width, initial-scale=1.0")

with doc.body:
    make_header()

    with d.main():
        with d.div(cls="featured"):
            make_all_featured()

print(doc)

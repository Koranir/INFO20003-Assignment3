import dominate
import dominate.tags as d


def make_doc(title):
    doc = dominate.document(title=f"Black Pepper Publishing - {title}")
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
    return doc

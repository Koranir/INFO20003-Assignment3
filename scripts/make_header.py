import dominate.tags as d


@d.header
def make_header():
    with d.div(cls="top"):
        with d.nav():
            d.a("Titles", href="/titles.html", cls="rim")
            d.a("Authors", href="/authors.html", cls="rim")
            d.a("Multimedia", href="/multimedia.html", cls="rim")
            d.a("About Us", href="/about.html", cls="rim")
            d.a("Submissions", href="/submissions.html", cls="rim")
            d.a("Cart", href="/cart.html", cls="rim")

        d.img(
            src="/assets/logo-rim.svg",
            alt="Black Pepper Publishing Logo",
        )
    d.input_(type="search", placeholder="Search books & more")

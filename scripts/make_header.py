import dominate.tags as d


@d.header
def make_header():
    with d.div(cls="top"):
        with d.nav():
            d.a("Titles", href="/titles.html")
            d.a("Authors", href="/authors.html")
            d.a("Multimedia", href="/multimedia.html")
            d.a("About Us", href="/about.html")
            d.a("Submissions", href="/submissions.html")
            d.a("Cart", href="/cart.html")

        d.img(
            cls="rim",
            src="/assets/logo.svg",
            alt="Black Pepper Publishing Logo",
        )
    d.input_(type="search", placeholder="Search books & more")

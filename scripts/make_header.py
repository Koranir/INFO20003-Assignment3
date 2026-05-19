import dominate.tags as d
import dominate.util as du


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
    with d.div(cls="search bold"):
        with d.button(cls="search-button"):
            du.raw(
                s='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-icon lucide-search"><path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/></svg>'
            )
        d.input_(
            type="search",
            placeholder="Search books & more",
            id="search-input",
        )

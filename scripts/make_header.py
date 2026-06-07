import dominate.tags as d
import dominate.util as du
from paths import asset_path, page_path


class dialog(d.html_tag):
    pass


@d.header
def make_header():
    with d.div(cls="desktop-top"):
        with d.nav():
            d.a("Titles", href=page_path("titles.html"), cls="rim")
            d.a("Authors", href=page_path("authors.html"), cls="rim")
            d.a("Multimedia", href=page_path("multimedia.html"), cls="rim")
            d.a("About Us", href=page_path("about.html"), cls="rim")
            d.a("Submissions", href=page_path("submissions.html"), cls="rim")
            d.a("Cart", href=page_path("cart.html"), cls="rim", id="cart-link")

        d.a(
            d.img(
                src=asset_path("logo-rim.svg"),
                alt="Black Pepper Publishing Logo",
            ),
            href=page_path("index.html"),
        )

    with d.div(cls="mobile-top"):
        with d.button(id="mobile-menu-button", onclick="toggleMobileMenu()"):
            d.img(
                src=asset_path("menu.svg"),
            )
        d.a(
            d.img(
                src=asset_path("logo-rim.svg"),
                alt="Black Pepper Publishing Logo",
            ),
            href=page_path("index.html"),
        )
        d.a(
            d.img(
                src=asset_path("cart-icon.svg"),
                alt="Shopping Cart Icon",
            ),
            href=page_path("cart.html"),
            id="cart-link-mobile",
        )

        with dialog(id="mobile-menu"):
            with d.button(id="mobile-menu-close", onclick="toggleMobileMenu()"):
                d.img(
                    src=asset_path("close.svg"),
                    alt="Close Menu Icon",
                )
            d.a("Titles", href=page_path("titles.html"), cls="rim")
            d.a("Authors", href=page_path("authors.html"), cls="rim")
            d.a("Multimedia", href=page_path("multimedia.html"), cls="rim")
            d.a("About Us", href=page_path("about.html"), cls="rim")
            d.a("Submissions", href=page_path("submissions.html"), cls="rim")
            d.a("Cart", href=page_path("cart.html"), cls="rim", id="cart-link")

    with d.div(cls="search bold", role="search"):
        with d.button(cls="search-button", type="button", **{"aria-label": "Search"}):
            du.raw(
                s='<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search-icon lucide-search"><path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/></svg>'
            )
        d.input_(
            type="search",
            placeholder="Search books & more",
            id="search-input",
            autocomplete="off",
            **{
                "aria-controls": "search-results",
                "aria-expanded": "false",
            },
        )
        d.div(id="search-results", cls="search-results", hidden=True)

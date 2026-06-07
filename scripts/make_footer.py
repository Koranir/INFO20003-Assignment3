import dominate.tags as d
from paths import asset_path, page_path


@d.div(cls="footer-area")
def make_footer():
    with d.footer():
        with d.div(cls="footer-links"):
            d.a("Submission Guidelies", href=page_path("submission-guidelines.html"))
            d.a("Privacy Policy", href=page_path("privacy-policy.html"))
            d.a("Terms and Conditions", href=page_path("terms-and-conditions.html"))
            d.a("Contact Us", href=page_path("contact.html"))
            d.a("Shipping Information", href=page_path("shipping-information.html"))
            d.a(
                "Rights & International Sales",
                href=page_path("rights-and-international-sales.html"),
            )
        with d.div(cls="footer-socials"):
            with d.div(cls="footer-mailing"):
                d.p("Want to be notified when new books come out?")
                with d.form(cls="footer-mailing-form"):
                    d.div(
                        d.input_(type="email", placeholder="your-email@gmail.com"),
                        cls="bold",
                    )
                    d.button("Join out mailing list »", type="submit", cls="bold")
            with d.div(cls="footer-social-icons"):
                d.a(
                    d.img(src=asset_path("twitter.svg"), alt="Twitter Logo"),
                    href="https://twitter.com/",
                )
                d.a(
                    d.img(src=asset_path("facebook.svg"), alt="Facebook Logo"),
                    href="https://www.facebook.com/p/Black-Pepper-Publishing-100068467657667/",
                )
                d.a(
                    d.img(src=asset_path("instagram.svg"), alt="Instagram Logo"),
                    href="https://www.instagram.com/",
                )
            d.p("© 2026 Black Pepper Publishing")

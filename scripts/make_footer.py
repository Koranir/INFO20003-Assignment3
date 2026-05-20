import dominate.tags as d


@d.div(cls="footer-area")
def make_footer():
    with d.footer():
        with d.div(cls="footer-links"):
            d.a("Submission Guidelies", href="/submission-guidelines.html")
            d.a("Privacy Policy", href="/privacy-policy.html")
            d.a("Terms and Conditions", href="/terms-and-conditions.html")
            d.a("Contact Us", href="/contact.html")
            d.a("Shipping Information", href="/shipping-information.html")
            d.a(
                "Rights & International Sales",
                href="/rights-and-international-sales.html",
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
                    d.img(src="/assets/twitter.svg", alt="Twitter Logo"),
                    href="https://twitter.com/",
                )
                d.a(
                    d.img(src="/assets/facebook.svg", alt="Facebook Logo"),
                    href="https://www.facebook.com/p/Black-Pepper-Publishing-100068467657667/",
                )
                d.a(
                    d.img(src="/assets/instagram.svg", alt="Instagram Logo"),
                    href="https://www.instagram.com/",
                )
            d.p("© 2026 Black Pepper Publishing")

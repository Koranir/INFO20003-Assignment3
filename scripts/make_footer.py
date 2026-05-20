import dominate.tags as d


def make_footer():
    with d.div(cls="footer"):
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

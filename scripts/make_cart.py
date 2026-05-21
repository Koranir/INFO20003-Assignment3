import dominate.tags as d
import dominate.util as du
from make_bestsellers import make_bestsellers
from make_doc import make_doc
from make_featured import make_all_featured
from make_footer import make_footer
from make_header import make_header
from make_recents import make_recents

doc = make_doc("Cart")
with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main():
            d.h2(
                "Cart",
                cls="section-title",
                style="--styled-asset-path: url('/assets/cart.svg')",
            )

            d.div(id="cart-items")

            with d.div(cls="billing"):
                with d.section():
                    d.h3("Billing Information")
                    with d.form(cls="billing-details"):
                        d.label("Email")
                        d.input_(type="email", name="email")

                        d.label("Title")
                        d.input_(type="text", name="title")

                        d.label("First Name")
                        d.input_(type="text", name="name")

                        d.label("Last Name")
                        d.input_(type="text", name="name")

                        d.label("Address")
                        d.input_(type="text", name="address")

                        d.label("Postcode")
                        d.input_(type="text", name="postcode")

                        d.label("City")
                        d.input_(type="text", name="city")

                        d.label("State")
                        d.input_(type="text", name="state")

                        d.label("Country")
                        d.input_(type="text", name="country")

                        d.label("Phone")
                        d.input_(type="tel", name="phone")
                with d.section(cls="order-summary"):
                    with d.table(cls="order-summary-table"):
                        with d.tbody():
                            d.tr(
                                d.td("Cart"),
                                d.td("A$ 0.00", id="cart-total"),
                            )
                            d.tr(
                                d.td("GST"),
                                d.td("A$ 0.00", id="cart-gst"),
                            )
                            d.tr(
                                d.td("Credit Surcharge"),
                                d.td("A$ 0.00", id="cart-surcharge"),
                            )
                            d.tr(
                                d.td("Shipping"),
                                d.td("A$ 0.00", id="cart-shipping"),
                            )
                with d.section(cls="grand-total"):
                    d.p("Total: A$ 0.00", id="cart-grand-total")
                with d.section(cls="checkout"):
                    d.h3("Pay With")
                    with d.div(cls="payment-options"):
                        d.button("PayPal", cls="payment-option")
                        d.button("Visa", cls="payment-option")
                        d.button("MasterCard", cls="payment-option")
                        d.button("Apple Pay", cls="payment-option")

    make_footer()

print(doc)

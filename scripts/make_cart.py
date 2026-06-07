import dominate.tags as d
from make_bestsellers import make_bestsellers
from make_doc import make_doc
from make_featured import make_all_featured
from make_footer import make_footer
from make_header import make_header
from make_recents import make_recents
from make_section_title import make_section_title
from paths import page_path

doc = make_doc("Cart")
with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main(cls="cart-page"):
            make_section_title("Cart", "cart.svg")

            with d.div(cls="billing-content-with-sidebar"):
                d.div(id="cart-items")

                with d.div(cls="billing-sidebar"):
                    with d.section(cls="billing-information"):
                        d.h3("Billing Information")
                        with d.form(
                            cls="billing-details",
                            id="billing-details",
                            action=page_path("order-confirmation.html"),
                            method="get",
                        ):
                            d.label("Email", fr="billing-email")
                            d.input_(
                                id="billing-email",
                                type="email",
                                name="email",
                                autocomplete="email",
                                required=True,
                            )

                            d.label("Title", fr="billing-title")
                            d.input_(
                                id="billing-title",
                                type="text",
                                name="title",
                                autocomplete="honorific-prefix",
                                maxlength=20,
                            )

                            d.label("First Name", fr="billing-first-name")
                            d.input_(
                                id="billing-first-name",
                                type="text",
                                name="first_name",
                                autocomplete="given-name",
                                required=True,
                            )

                            d.label("Last Name", fr="billing-last-name")
                            d.input_(
                                id="billing-last-name",
                                type="text",
                                name="last_name",
                                autocomplete="family-name",
                                required=True,
                            )

                            d.label("Address", fr="billing-address")
                            d.input_(
                                id="billing-address",
                                type="text",
                                name="address",
                                autocomplete="street-address",
                                required=True,
                            )

                            d.label("Postcode", fr="billing-postcode")
                            d.input_(
                                id="billing-postcode",
                                type="text",
                                name="postcode",
                                autocomplete="postal-code",
                                pattern="[A-Za-z0-9][A-Za-z0-9 -]{2,9}",
                                maxlength=10,
                                title="Enter a valid postcode",
                                required=True,
                            )

                            d.label("City", fr="billing-city")
                            d.input_(
                                id="billing-city",
                                type="text",
                                name="city",
                                autocomplete="address-level2",
                                required=True,
                            )

                            d.label("State", fr="billing-state")
                            d.input_(
                                id="billing-state",
                                type="text",
                                name="state",
                                autocomplete="address-level1",
                                required=True,
                            )

                            d.label("Country", fr="billing-country")
                            d.input_(
                                id="billing-country",
                                type="text",
                                name="country",
                                autocomplete="country-name",
                                required=True,
                            )

                            d.label("Phone", fr="billing-phone")
                            d.input_(
                                id="billing-phone",
                                type="tel",
                                name="phone",
                                autocomplete="tel",
                                pattern=r"[0-9()+\-\s]{8,20}",
                                title="Use 8 to 20 digits, spaces, or phone symbols",
                                required=True,
                            )
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
                    for label, value in (
                        ("PayPal", "paypal"),
                        ("Visa", "visa"),
                        ("MasterCard", "mastercard"),
                        ("Apple Pay", "apple_pay"),
                    ):
                        d.button(
                            label,
                            type="submit",
                            form="billing-details",
                            name="payment_method",
                            value=value,
                            cls="purchase bold",
                        )

    make_footer()

print(doc)

import dominate.tags as d
from make_bestsellers import make_bestsellers
from make_doc import make_doc
from make_featured import make_all_featured
from make_footer import make_footer
from make_header import make_header
from make_recents import make_recents
from paths import asset_path, page_path

doc = make_doc("Order Confirmation")
with doc.body:
    with d.div(cls="content-area"):
        make_header()

        with d.main(cls="cart-page"):
            d.h2(
                "Order Confirmed",
                cls="section-title",
                style=f"--styled-asset-path: url('{asset_path('order-confirmed.svg')}')",
            )

            with d.section(cls="order-confirmation"):
                d.p("Your order is now being processed:")
                with d.table():
                    d.tbody(id="order-confirmation-table-body")
                d.p("An email will be sent when the order is finalised.")

                with d.div(cls="confirmation-cancel-okay"):
                    d.a("Cancel Order", href=page_path("index.html"), cls="bold warning")
                    d.button("Okay", onclick="orderConfirmed()", cls="bold purchase")

    make_footer()

print(doc)

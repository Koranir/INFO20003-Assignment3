class Cart {
    constructor() {
        /** @type {Object.<string, number>} */
        this.cart = {};
    }

    syncCart() {
        const stored = localStorage.getItem("cart");
        if (stored) {
            this.cart = JSON.parse(stored);
        } else {
            this.cart = {};
        }
    }

    /**
     * @param {String} product_id
     * @param {number} count
     */
    add(product_id, count) {
        this.syncCart();

        if (this.cart[product_id]) {
            this.cart[product_id] += count;
        } else {
            this.cart[product_id] = count;
        }

        localStorage.setItem("cart", JSON.stringify(this.cart));
    }

    /**
     * @param {String} product_id
     * @return {number}
     */
    get(product_id) {
        this.syncCart();

        return this.cart[product_id] || 0;
    }

    /**
     * @return {Object.<string, number>}
     */
    items() {
        this.syncCart();
        return this.cart;
    }
}

function updateCartItemCount() {
    const element = document.getElementById("cart-link");
    if (element) {
        const cart = new Cart();
        var count = 0;

        for (const item_count of Object.values(cart.items())) {
            count += item_count;
        }

        element.textContent = `Cart (${count})`;
    } else {
        console.warn("No cart element");
    }
}

function setupRecentReleases() {
    const recentButtons = Array.from(
        document.querySelectorAll(".recent-title"),
    );
    const releases = recentButtons.map((button) =>
        button.id.replace("recent-title-", ""),
    );

    function selectRecentRelease(selectedRelease) {
        releases.forEach((release) => {
            const isSelected = release === selectedRelease;
            document
                .getElementById(`recent-cover-${release}`)
                ?.toggleAttribute("hidden", !isSelected);
            document
                .getElementById(`recent-description-${release}`)
                ?.toggleAttribute("hidden", !isSelected);
        });

        recentButtons.forEach((button) => {
            const isSelected = button.id === `recent-title-${selectedRelease}`;
            if (isSelected) {
                button.setAttribute("x-checked", "true");
            } else {
                button.removeAttribute("x-checked");
            }
            button.setAttribute("aria-pressed", String(isSelected));
        });
    }

    recentButtons.forEach((button) => {
        button.addEventListener("click", () => {
            selectRecentRelease(button.id.replace("recent-title-", ""));
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    updateCartItemCount();
    setupRecentReleases();
});

/**
 * @param {string} item
 * @param {{title?: string, author?: string, price?: string | number}} details
 */
function showAddedToCartDialog(item, details = {}) {
    const existingDialog = document.querySelector(".cart-dialog");
    if (existingDialog) {
        existingDialog.remove();
    }

    const productTitle =
        details.title ||
        document.querySelector(".product-header .section-title")?.textContent.trim() ||
        item;
    const productAuthor =
        details.author ||
        document.querySelector(".product-header .section-subtitle")?.textContent.trim() ||
        "";
    const productPrice =
        details.price ||
        document.querySelector(".purchase .price")?.textContent.replace("A$ ", "") ||
        "";

    const cartDialog = document.createElement("dialog");
    cartDialog.setAttribute("class", "cart-dialog");
    cartDialog.innerHTML = `
        <h3>Added to Cart</h3>
        <div class="cart-dialog-product">
            <img
                src="/assets/books/${item}/cover.jpg"
                alt="Cover of ${productTitle}"
            >
            <div class="cart-dialog-details">
                <strong>${productTitle}</strong>
                <span>${productAuthor}</span>
            </div>
            <span class="cart-dialog-price">A$ ${productPrice}</span>
        </div>
        <div class="cart-dialog-actions">
            <a href="/cart.html" class="bold">View Cart &raquo;</a>
            <button type="button" class="bold" value="cancel">Continue Browsing</button>
        </div>
    `;

    cartDialog
        .querySelector("button")
        .addEventListener("click", () => cartDialog.close());
    cartDialog.addEventListener("close", () => cartDialog.remove());

    document.body.append(cartDialog);
    cartDialog.showModal();
}

/**
 * @param {string} item
 * @param {number} count
 * @param {{title?: string, author?: string, price?: string | number}} details
 */
function addToCart(item, count, details = {}) {
    new Cart().add(item, count);
    updateCartItemCount();
    showAddedToCartDialog(item, details);
}

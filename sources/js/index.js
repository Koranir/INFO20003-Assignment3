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
    const cart = new Cart();
    var count = 0;

    for (const item_count of Object.values(cart.items())) {
        count += item_count;
    }

    for (const element of document.querySelectorAll("#cart-link")) {
        element.textContent = `Cart (${count})`;
    }
}

/**
 * @param {number} value
 * @return {string}
 */
function formatCurrency(value) {
    return `A$ ${value.toFixed(2)}`;
}

/**
 * @return {Promise<Object.<string, {title: string, author: string, price: number}>>}
 */
async function getCartProducts() {
    const response = await fetch("/data/cart-products.json");
    if (!response.ok) {
        throw new Error(`Failed to load cart products: ${response.status}`);
    }

    return response.json();
}

/**
 * @param {string} id
 * @param {string} text
 */
function setText(id, text) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = text;
    }
}

/**
 * @return {Array<[string, number]>}
 */
function getCartEntries() {
    const cart = new Cart();
    return Object.entries(cart.items()).filter(([, count]) => count > 0);
}

/**
 * @param {number} total
 */
function updateCartTotals(total) {
    const gst = total * 0.1;
    const surcharge = 0;
    const shipping = 0;
    const grandTotal = total + gst + surcharge + shipping;

    setText("cart-total", formatCurrency(total));
    setText("cart-gst", formatCurrency(gst));
    setText("cart-surcharge", formatCurrency(surcharge));
    setText("cart-shipping", formatCurrency(shipping));
    setText("cart-grand-total", `Total: ${formatCurrency(grandTotal)}`);
}

async function setupCartPage() {
    const cartItems = document.getElementById("cart-items");
    if (!cartItems) {
        return;
    }

    const entries = getCartEntries();

    cartItems.replaceChildren();

    if (entries.length === 0) {
        const emptyMessage = document.createElement("p");
        emptyMessage.textContent = "Your cart is empty.";
        cartItems.append(emptyMessage);
        updateCartTotals(0);
        return;
    }

    let products;
    try {
        products = await getCartProducts();
    } catch (error) {
        console.error(error);
        const errorMessage = document.createElement("p");
        errorMessage.textContent = "Cart products could not be loaded.";
        cartItems.append(errorMessage);
        updateCartTotals(0);
        return;
    }

    let cartTotal = 0;

    entries.forEach(([productId, count]) => {
        const product = products[productId];
        if (!product) {
            return;
        }

        const price = Number(product.price);
        const itemTotal = price * count;
        cartTotal += itemTotal;

        const item = document.createElement("section");
        item.className = "cart-item";

        const cover = document.createElement("img");
        cover.src = `/assets/books/${productId}/cover.jpg`;
        cover.alt = `Cover of ${product.title}`;

        const details = document.createElement("div");
        details.className = "cart-item-details";

        const title = document.createElement("h3");
        title.textContent = product.title;

        const author = document.createElement("p");
        author.textContent = product.author;

        details.append(title, author);

        const totals = document.createElement("table");
        totals.className = "cart-item-totals";
        const totalsBody = document.createElement("tbody");

        [
            ["Price", formatCurrency(price)],
            ["Copies", String(count)],
            ["Total", formatCurrency(itemTotal)],
        ].forEach(([label, value]) => {
            const row = document.createElement("tr");
            const heading = document.createElement("th");
            const cell = document.createElement("td");

            heading.scope = "row";
            heading.textContent = label;
            cell.textContent = value;

            row.append(heading, cell);
            totalsBody.append(row);
        });

        totals.append(totalsBody);
        item.append(cover, details, totals);
        cartItems.append(item);
    });

    updateCartTotals(cartTotal);
}

async function setupOrderConfirmationPage() {
    const orderConfirmationTableBody = document.getElementById(
        "order-confirmation-table-body",
    );
    if (!orderConfirmationTableBody) {
        return;
    }

    const entries = getCartEntries();
    let products = {};

    try {
        products = await getCartProducts();
    } catch (error) {
        console.error(error);
    }

    orderConfirmationTableBody.replaceChildren();

    let totalCost = 0;

    entries.forEach(([productId, count]) => {
        const price = Number(products[productId]?.price || 0);
        totalCost += price * count;

        const row = document.createElement("tr");
        const title = document.createElement("td");
        const itemCount = document.createElement("td");

        title.scope = "row";
        title.textContent = products[productId]?.title || productId;
        itemCount.textContent = "x" + String(count);

        row.append(title, itemCount);
        orderConfirmationTableBody.append(row);
    });

    const totalRow = document.createElement("tr");
    const totalHeading = document.createElement("td");
    const totalCell = document.createElement("td");

    totalHeading.scope = "row";
    totalHeading.textContent = "Total";
    totalCell.textContent = formatCurrency(totalCost);

    totalRow.append(totalHeading, totalCell);
    orderConfirmationTableBody.append(totalRow);
}

function setupRecentReleases() {
    const recentButtons = Array.from(
        document.querySelectorAll(".recent-title"),
    );
    if (recentButtons.length === 0) {
        return;
    }

    const releases = recentButtons.map((button) =>
        button.id.replace("recent-title-", ""),
    );
    const descriptionContainer = document.querySelector(".recent-descriptions");
    const prefersReducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)",
    );
    let currentRelease =
        recentButtons
            .find((button) => button.getAttribute("x-checked") === "true")
            ?.id.replace("recent-title-", "") || releases[0];
    let autoCycleTimeoutId = null;
    let autoCycleStopped = false;

    function setReleasePanelState(element, isSelected) {
        if (!element) {
            return;
        }

        element.dataset.state = isSelected ? "active" : "inactive";
        element.removeAttribute("hidden");
        element.setAttribute("aria-hidden", String(!isSelected));

        if (element.classList.contains("recent-description")) {
            element.toggleAttribute("inert", !isSelected);
        }
    }

    function updateDescriptionContainerHeight(selectedRelease) {
        if (!descriptionContainer) {
            return;
        }

        const activeDescription = document.getElementById(
            `recent-description-${selectedRelease}`,
        );
        if (!activeDescription) {
            return;
        }

        descriptionContainer.style.height = `${activeDescription.scrollHeight}px`;
    }

    function selectRecentRelease(selectedRelease) {
        currentRelease = selectedRelease;

        releases.forEach((release) => {
            const isSelected = release === selectedRelease;
            setReleasePanelState(
                document.getElementById(`recent-cover-${release}`),
                isSelected,
            );
            setReleasePanelState(
                document.getElementById(`recent-description-${release}`),
                isSelected,
            );
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

        updateDescriptionContainerHeight(selectedRelease);
    }

    function clearAutoCycle() {
        if (autoCycleTimeoutId === null) {
            return;
        }

        window.clearTimeout(autoCycleTimeoutId);
        autoCycleTimeoutId = null;
    }

    function scheduleNextAutoCycle() {
        clearAutoCycle();

        if (
            autoCycleStopped ||
            prefersReducedMotion.matches ||
            document.hidden ||
            releases.length < 2
        ) {
            return;
        }

        autoCycleTimeoutId = window.setTimeout(() => {
            const currentIndex = releases.indexOf(currentRelease);
            const nextIndex = (currentIndex + 1) % releases.length;
            selectRecentRelease(releases[nextIndex]);
            scheduleNextAutoCycle();
        }, 5000);
    }

    selectRecentRelease(currentRelease);
    descriptionContainer?.classList.add("is-ready");
    updateDescriptionContainerHeight(currentRelease);

    recentButtons.forEach((button) => {
        button.addEventListener("click", () => {
            autoCycleStopped = true;
            clearAutoCycle();
            selectRecentRelease(button.id.replace("recent-title-", ""));
        });
    });

    document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
            clearAutoCycle();
            return;
        }

        scheduleNextAutoCycle();
    });

    window.addEventListener("resize", () => {
        updateDescriptionContainerHeight(currentRelease);
    });

    scheduleNextAutoCycle();
}

document.addEventListener("DOMContentLoaded", () => {
    updateCartItemCount();
    setupCartPage();
    setupOrderConfirmationPage();
    setupRecentReleases();
});

/**
 * Show a modal dialog confirming a particular item with this id was added to the cart.
 * TODO: Use the JSON product data instead of scraping the page, this is an old impl.
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
        document
            .querySelector(".product-header .section-title")
            ?.textContent.trim() ||
        item;
    const productAuthor =
        details.author ||
        document
            .querySelector(".product-header .section-subtitle")
            ?.textContent.trim() ||
        "";
    const productPrice =
        details.price ||
        document
            .querySelector(".purchase .price")
            ?.textContent.replace("A$ ", "") ||
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
 * Add an item to the cart, showing a dialog.
 * @param {string} item
 * @param {number} count
 * @param {{title?: string, author?: string, price?: string | number}} details
 */
function addToCart(item, count, details = {}) {
    new Cart().add(item, count);
    updateCartItemCount();
    showAddedToCartDialog(item, details);
}

/**
 * Clear the cart after an order is confirmed, to emulate a successful checkout.
 */
function orderConfirmed() {
    localStorage.removeItem("cart");

    // Move to the home page after we're done
    location.href = "/";
}

/**
 * Toggle the mobile menu.
 */
function toggleMobileMenu() {
    const menu = document.getElementById("mobile-menu");
    if (menu.open) {
        menu.close();
    } else {
        menu.showModal();
    }
}

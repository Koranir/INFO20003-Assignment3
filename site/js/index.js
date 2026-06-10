const SCRIPT_SRC = document.currentScript?.getAttribute("src") || "";
const SITE_ROOT = SCRIPT_SRC.match(/^(.*)js\/index\.js$/)?.[1] || "";

/**
 * @param {string} path
 * @return {string}
 */
function sitePath(path) {
    return SITE_ROOT + path;
}

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
            this.cart[product_id] += Number(count);
        } else {
            this.cart[product_id] = Number(count);
        }

        localStorage.setItem("cart", JSON.stringify(this.cart));
    }

    /**
     * @param {String} product_id
     * @param {number} new_count
     */
    set(product_id, count) {
        this.syncCart();

        if (count == 0) {
            delete this.cart[product_id];
        } else {
            this.cart[product_id] = Number(count);
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

let cartProductsCache = null;

/**
 * @return {Promise<Object.<string, {title: string, author: string, price: number}>>}
 */
async function getCartProducts() {
    if (!cartProductsCache) {
        cartProductsCache = fetch(sitePath("data/cart-products.json")).then(
            (response) => {
                if (!response.ok) {
                    throw new Error(
                        `Failed to load cart products: ${response.status}`,
                    );
                }

                return response.json();
            },
        );
    }

    return cartProductsCache;
}

const SEARCH_RESULT_LIMIT = 8;

/**
 * @param {Object.<string, {title: string, author: string, price: number}>} products
 * @param {string} query
 * @return {Array<{id: string, title: string, author: string}>}
 */
function getTitleSearchResults(products, query) {
    const trimmedQuery = query.trim();
    if (!trimmedQuery) {
        return [];
    }

    const items = Object.entries(products).map(([id, product]) => ({
        id,
        title: product.title,
        author: product.author || "",
    }));
    const lowerQuery = trimmedQuery.toLowerCase();
    const fragments = lowerQuery.split(/\s+/).filter(Boolean);
    const seen = new Set();

    const byStartIndexThenTitle = (left, right) =>
        left.startIndex - right.startIndex ||
        left.item.title.localeCompare(right.item.title);

    // const exactCaseMatches = items
    //     .map((item) => ({
    //         item,
    //         startIndex: item.title.indexOf(trimmedQuery),
    //     }))
    //     .filter((match) => match.startIndex !== -1)
    //     .sort(byStartIndexThenTitle);

    // exactCaseMatches.forEach((match) => seen.add(match.item.id));

    const exactCaseInsensitiveMatches = items
        .map((item) => ({
            item,
            startIndex: item.title.toLowerCase().indexOf(lowerQuery),
        }))
        .filter((match) => match.startIndex !== -1 && !seen.has(match.item.id))
        .sort(byStartIndexThenTitle);

    exactCaseInsensitiveMatches.forEach((match) => seen.add(match.item.id));

    const approximateMatches = items
        .filter(
            (item) =>
                !seen.has(item.id) &&
                fragments.every((fragment) =>
                    item.title.toLowerCase().includes(fragment),
                ),
        )
        .sort((left, right) => left.title.localeCompare(right.title))
        .map((item) => ({ item }));

    return [
        // ...exactCaseMatches,
        ...exactCaseInsensitiveMatches,
        ...approximateMatches,
    ]
        .slice(0, SEARCH_RESULT_LIMIT)
        .map((match) => match.item);
}

function setupHeaderSearch() {
    const input = document.getElementById("search-input");
    const resultsPanel = document.getElementById("search-results");

    if (!input || !resultsPanel) {
        return;
    }

    const searchContainer = input.closest(".search");
    if (!searchContainer) {
        return;
    }

    const searchButton = searchContainer.querySelector(".search-button");

    let products = {};
    let hasLoadedProducts = false;
    let hasLoadError = false;
    let currentResults = [];

    function setExpanded(isExpanded) {
        input.setAttribute("aria-expanded", String(isExpanded));
    }

    function closeResults() {
        resultsPanel.hidden = true;
        setExpanded(false);
    }

    function openResults() {
        resultsPanel.hidden = false;
        setExpanded(true);
    }

    /**
     * @param {string} message
     */
    function renderSearchMessage(message) {
        const emptyMessage = document.createElement("p");
        emptyMessage.className = "search-empty";
        emptyMessage.textContent = message;
        resultsPanel.replaceChildren(emptyMessage);
        currentResults = [];
        openResults();
    }

    function renderResults() {
        const query = input.value.trim();
        resultsPanel.replaceChildren();

        if (!query) {
            currentResults = [];
            closeResults();
            return;
        }

        if (hasLoadError) {
            renderSearchMessage("Search is unavailable.");
            return;
        }

        if (!hasLoadedProducts) {
            renderSearchMessage("Loading results...");
            return;
        }

        currentResults = getTitleSearchResults(products, query);

        if (currentResults.length === 0) {
            renderSearchMessage("No matching titles.");
            return;
        }

        currentResults.forEach((result) => {
            const resultLink = document.createElement("a");
            resultLink.className = "search-result";
            resultLink.href = sitePath(`products/${result.id}.html`);

            const cover = document.createElement("img");
            cover.className = "search-result-cover";
            cover.src = sitePath(`assets/books/${result.id}/cover.jpg`);
            cover.alt = `Cover of ${result.title}`;

            const details = document.createElement("span");
            details.className = "search-result-details";

            const title = document.createElement("span");
            title.className = "search-result-title";
            title.textContent = result.title;

            const author = document.createElement("span");
            author.className = "search-result-author";
            author.textContent = result.author;

            details.append(title, author);
            resultLink.append(cover, details);
            resultsPanel.append(resultLink);
        });

        openResults();
    }

    /**
     * @return {HTMLAnchorElement[]}
     */
    function getResultLinks() {
        return Array.from(resultsPanel.querySelectorAll(".search-result"));
    }

    /**
     * @param {number} fallbackIndex
     * @param {number} offset
     */
    function focusResult(fallbackIndex, offset = 0) {
        const resultLinks = getResultLinks();

        if (resultLinks.length === 0) {
            return;
        }

        const focusedIndex = resultLinks.indexOf(document.activeElement);
        const nextIndex =
            focusedIndex === -1
                ? fallbackIndex
                : (focusedIndex + offset + resultLinks.length) %
                  resultLinks.length;

        resultLinks[nextIndex].focus();
    }

    input.addEventListener("input", renderResults);
    input.addEventListener("focus", renderResults);
    input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeResults();
            return;
        }

        if (event.key === "ArrowDown") {
            if (resultsPanel.hidden) {
                renderResults();
            }

            if (currentResults.length > 0) {
                event.preventDefault();
                focusResult(0);
            }
            return;
        }

        if (event.key === "ArrowUp") {
            if (currentResults.length > 0) {
                event.preventDefault();
                focusResult(currentResults.length - 1);
            }
        }
    });

    resultsPanel.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            input.focus();
            closeResults();
            return;
        }

        if (event.key === "ArrowDown") {
            event.preventDefault();
            focusResult(0, 1);
            return;
        }

        if (event.key === "ArrowUp") {
            event.preventDefault();
            focusResult(currentResults.length - 1, -1);
        }
    });

    searchButton?.addEventListener("click", () => {
        input.focus();
        renderResults();
    });

    document.addEventListener("pointerdown", (event) => {
        if (
            !(event.target instanceof Element) ||
            !searchContainer.contains(event.target)
        ) {
            closeResults();
        }
    });

    searchContainer.addEventListener("focusout", (event) => {
        if (
            !(event.relatedTarget instanceof Element) ||
            !searchContainer.contains(event.relatedTarget)
        ) {
            closeResults();
        }
    });

    getCartProducts()
        .then((loadedProducts) => {
            products = loadedProducts;
            hasLoadedProducts = true;
            renderResults();
        })
        .catch((error) => {
            console.error(error);
            hasLoadError = true;
            renderResults();
        });
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
        cover.src = sitePath(`assets/books/${productId}/cover.jpg`);
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

            if (label === "Copies") {
                const input = document.createElement("input");
                input.setAttribute("type", "number");
                input.setAttribute("min", "1");
                input.setAttribute("step", "1");
                input.setAttribute("value", value);

                input.addEventListener("change", (event) => {
                    console.log(
                        "Updating cart:",
                        productId,
                        event.target.value,
                    );
                    new Cart().set(productId, event.target.value);
                    setupCartPage();
                    updateCartItemCount();
                });

                cell.append(input);
            } else {
                cell.textContent = value;
            }

            row.append(heading, cell);
            totalsBody.append(row);
        });

        const deleteButton = document.createElement("button");
        deleteButton.className = "bold";
        deleteButton.textContent = "Delete";
        const delButtonRow = document.createElement("tr");
        const delButtonCell = document.createElement("td");
        delButtonCell.colSpan = 2;
        delButtonCell.append(deleteButton);
        delButtonRow.append(delButtonCell);

        deleteButton.addEventListener("click", () => {
            new Cart().set(productId, 0);
            setupCartPage();
            updateCartItemCount();
        });
        totalsBody.append(delButtonRow);

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
    setupHeaderSearch();
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
        <div class="cart-dialog-header">
            <div></div>
            <h3>Added to Cart</h3>
            <button type="button" value="cancel"><img src="${sitePath("assets/close.svg")}"></img></button>
        </div>
        <div class="cart-dialog-product">
            <img
                src="${sitePath(`assets/books/${item}/cover.jpg`)}"
                alt="Cover of ${productTitle}"
            >
            <div class="cart-dialog-details">
                <strong>${productTitle}</strong>
                <span>${productAuthor}</span>
            </div>
            <span class="cart-dialog-price">A$ ${productPrice}</span>
        </div>
        <div class="cart-dialog-actions">
            <a href="${sitePath("cart.html")}" class="bold">View Cart &raquo;</a>
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
    location.href = sitePath("index.html");
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

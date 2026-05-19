"use strict";

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

document.addEventListener("DOMContentLoaded", updateCartItemCount);

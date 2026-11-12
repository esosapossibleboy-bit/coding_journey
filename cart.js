function calculateCartTotal(price, quantity, tax) {
    const subtotal = price * quantity;
    const total = subtotal + tax;
    return total;
}

// This lets our automated referee borrow this function!
module.exports = { calculateCartTotal };
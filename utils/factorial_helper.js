function calculateFactorial(n) {
    if (typeof n !== 'number' || n < 0 || !Number.isInteger(n)) return 0;
    if (n === 0) return 1;
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

module.exports = { calculateFactorial };

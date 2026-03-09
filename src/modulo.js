/**
 * Returns the modulo (remainder) of two numbers.
 * @param {number} a - Dividend
 * @param {number} b - Divisor
 * @returns {number} The remainder of a divided by b
 */
function modulo(a, b) {
  if (b === 0) throw new Error('Cannot divide by zero');
  return a % b;
}

module.exports = modulo;

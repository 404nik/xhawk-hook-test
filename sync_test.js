function add(a, b) { return a + b; }
function subtract(a, b) { return a - b; }
function multiply(a, b) { return a * b; }
function divide(a, b) { return b !== 0 ? a / b : null; }
function power(a, b) { return Math.pow(a, b); }
function modulo(a, b) { return b !== 0 ? a % b : null; }
function max(a, b) { return a > b ? a : b; }
function min(a, b) { return a < b ? a : b; }
function abs(a) { return a < 0 ? -a : a; }
function factorial(n) {
  if (n < 0) return null;
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}

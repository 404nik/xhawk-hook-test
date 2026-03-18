function clamp(value, min, max) {
  if (typeof value !== 'number' || typeof min !== 'number' || typeof max !== 'number') {
    return NaN;
  }
  if (min > max) {
    const temp = min;
    min = max;
    max = temp;
  }
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

function average(numbers) {
  if (!Array.isArray(numbers) || numbers.length === 0) {
    return NaN;
  }
  let sum = 0;
  let count = 0;
  for (const n of numbers) {
    if (typeof n === 'number' && !Number.isNaN(n)) {
      sum += n;
      count += 1;
    }
  }
  if (count === 0) {
    return NaN;
  }
  return sum / count;
}

function isPrime(n) {
  if (typeof n !== 'number' || !Number.isInteger(n) || n <= 1) {
    return false;
  }
  if (n <= 3) {
    return true;
  }
  if (n % 2 === 0 || n % 3 === 0) {
    return false;
  }
  for (let i = 5; i * i <= n; i += 6) {
    if (n % i === 0 || n % (i + 2) === 0) {
      return false;
    }
  }
  return true;
}

function factorial(n) {
  if (typeof n !== 'number' || !Number.isInteger(n) || n < 0) {
    return NaN;
  }
  if (n === 0 || n === 1) {
    return 1;
  }
  return n * factorial(n - 1);
}

function fibonacci(n) {
  if (typeof n !== 'number' || !Number.isInteger(n) || n < 0) {
    return NaN;
  }
  if (n === 0) {
    return 0;
  }
  if (n === 1) {
    return 1;
  }
  return fibonacci(n - 1) + fibonacci(n - 2);
}

module.exports = {
  clamp,
  average,
  isPrime,
  factorial,
  fibonacci,
};

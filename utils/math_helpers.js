function calculateAverage(numbers) {
  if (!numbers.length) return 0;
  return numbers.reduce((sum, n) => sum + n, 0) / numbers.length;
}

module.exports = { calculateAverage };

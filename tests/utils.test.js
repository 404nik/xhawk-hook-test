const { truncateString } = require('../utils/text_utils');
const { clamp, isPrime, average } = require('../utils/math_utils');

// Tests for truncateString
console.assert(
  truncateString('Hello World', 5) === 'He...',
  'truncateString should truncate and add ellipsis'
);
console.assert(
  truncateString('Hi', 5) === 'Hi',
  'truncateString should not truncate short strings'
);

// Tests for clamp
console.assert(
  clamp(5, 1, 10) === 5,
  'clamp should return value within range'
);
console.assert(
  clamp(-1, 0, 10) === 0,
  'clamp should clamp value below min to min'
);
console.assert(
  clamp(20, 0, 10) === 10,
  'clamp should clamp value above max to max'
);

// Tests for isPrime
console.assert(
  isPrime(7) === true,
  'isPrime should identify prime numbers'
);
console.assert(
  isPrime(8) === false,
  'isPrime should identify non-prime numbers'
);

// Tests for average
console.assert(
  average([1, 2, 3, 4, 5]) === 3,
  'average should compute the mean of numbers'
);
console.assert(
  Number.isNaN(average([])),
  'average should be NaN for empty array'
);

console.log('All utils tests passed.');


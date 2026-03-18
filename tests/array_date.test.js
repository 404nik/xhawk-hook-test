const { flattenArray, uniqueValues, chunkArray } = require('../utils/array_utils');
const { daysBetween, isWeekend } = require('../utils/temporal_utils');

// flattenArray tests
console.assert(JSON.stringify(flattenArray([1, [2, 3], [4]])) === '[1,2,3,4]', 'flattenArray: basic nested arrays');
console.assert(JSON.stringify(flattenArray([[1], [2], [3]])) === '[1,2,3]', 'flattenArray: single-element arrays');
console.assert(JSON.stringify(flattenArray([])) === '[]', 'flattenArray: empty array');

// uniqueValues tests
console.assert(JSON.stringify(uniqueValues([1, 2, 2, 3, 3, 3])) === '[1,2,3]', 'uniqueValues: removes duplicates');
console.assert(JSON.stringify(uniqueValues([1, 2, 3])) === '[1,2,3]', 'uniqueValues: no duplicates');
console.assert(JSON.stringify(uniqueValues([])) === '[]', 'uniqueValues: empty array');

// chunkArray tests
console.assert(JSON.stringify(chunkArray([1, 2, 3, 4, 5], 2)) === '[[1,2],[3,4],[5]]', 'chunkArray: uneven chunks');
console.assert(JSON.stringify(chunkArray([1, 2, 3, 4], 2)) === '[[1,2],[3,4]]', 'chunkArray: even chunks');
console.assert(JSON.stringify(chunkArray([], 3)) === '[]', 'chunkArray: empty array');

// daysBetween tests
console.assert(daysBetween(new Date('2024-01-01'), new Date('2024-01-11')) === 10, 'daysBetween: 10 days apart');
console.assert(daysBetween(new Date('2024-03-01'), new Date('2024-03-01')) === 0, 'daysBetween: same date');
console.assert(daysBetween(new Date('2024-01-11'), new Date('2024-01-01')) === 10, 'daysBetween: reverse order');

// isWeekend tests
console.assert(isWeekend(new Date('2024-03-16')) === true, 'isWeekend: Saturday');
console.assert(isWeekend(new Date('2024-03-17')) === true, 'isWeekend: Sunday');
console.assert(isWeekend(new Date('2024-03-15')) === false, 'isWeekend: Friday');
console.assert(isWeekend(new Date('2024-03-18')) === false, 'isWeekend: Monday');

console.log('All tests passed!');

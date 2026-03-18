/**
 * @module array_utils
 * @description Utility functions for common array operations including
 * flattening, deduplication, chunking, and grouping.
 */

function flattenArray(arr) {
  return [].concat(...arr);
}

function uniqueValues(arr) {
  return [...new Set(arr)];
}

function chunkArray(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
}

function groupBy(arr, keyFn) {
  return arr.reduce((groups, item) => {
    const key = keyFn(item);
    if (!groups[key]) groups[key] = [];
    groups[key].push(item);
    return groups;
  }, {});
}

module.exports = { flattenArray, uniqueValues, chunkArray, groupBy };

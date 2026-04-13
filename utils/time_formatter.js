/**
 * Formats a given timestamp to an ISO string.
 * @param {number|string|Date} ts - The timestamp to format.
 * @returns {string} The ISO formatted string.
 */
function formatTimestampToISO(ts) {
  return new Date(ts).toISOString();
}

module.exports = {
  formatTimestampToISO,
};

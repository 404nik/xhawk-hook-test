/**
 * Checks if a string contains only letters (a-z, A-Z).
 * @param {string} text - The text to check.
 * @returns {boolean} True if the string contains only letters, false otherwise.
 */
function isAlphabetOnly(text) {
  if (typeof text !== 'string' || text.length === 0) {
    return false;
  }
  return /^[a-zA-Z]+$/.test(text);
}

module.exports = {
  isAlphabetOnly,
};

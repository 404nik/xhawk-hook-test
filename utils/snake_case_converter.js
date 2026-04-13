/**
 * Converts a string to snake_case.
 * @param {string} text - The text to convert.
 * @returns {string} The snake_case formatted string.
 */
function convertToSnakeCase(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, '') // Remove special characters
    .replace(/\s+/g, '_');      // Convert spaces to underscores
}

module.exports = {
  convertToSnakeCase,
};

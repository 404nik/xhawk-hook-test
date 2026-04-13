/**
 * Generates a random UUID-like string.
 * This is a simplified implementation for generating a UUID v4-style string without external dependencies.
 * @returns {string} A random UUID-like string.
 */
function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

module.exports = {
  generateUUID,
};

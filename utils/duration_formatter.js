/**
 * Converts a number of seconds into a human readable duration string.
 * @param {number} seconds - The number of seconds to format.
 * @returns {string} The human readable duration (e.g., "1h 20m 35s").
 */
function formatSecondsToDuration(seconds) {
  if (seconds < 0) return "0s";
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (remainingSeconds > 0 || parts.length === 0) parts.push(`${remainingSeconds}s`);

  return parts.join(" ");
}

module.exports = {
  formatSecondsToDuration,
};

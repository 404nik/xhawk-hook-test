function isPalindrome(str) {
  if (typeof str !== 'string') return false;
  const normalized = str.toLowerCase();
  const reversed = normalized.split('').reverse().join('');
  return normalized === reversed;
}

module.exports = { isPalindrome };

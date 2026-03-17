function truncateString(str, maxLength) {
  if (typeof str !== 'string') {
    return '';
  }
  if (typeof maxLength !== 'number' || maxLength <= 0) {
    return '';
  }
  if (str.length <= maxLength) {
    return str;
  }
  if (maxLength <= 3) {
    return '.'.repeat(maxLength);
  }
  return str.slice(0, maxLength - 3) + '...';
}

function capitalizeWords(str) {
  if (typeof str !== 'string') {
    return '';
  }
  return str
    .split(/\s+/)
    .filter(Boolean)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

function countWords(str) {
  if (typeof str !== 'string') {
    return 0;
  }
  const matches = str.trim().match(/\S+/g);
  return matches ? matches.length : 0;
}

function reverseString(str) {
  if (typeof str !== 'string') {
    return '';
  }
  return str.split('').reverse().join('');
}

module.exports = {
  truncateString,
  capitalizeWords,
  countWords,
  reverseString,
};

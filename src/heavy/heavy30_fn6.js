// Heavy batch 30 - Function 6 (1773095464543885000)
function heavy30_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy30_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn6(input, 6);
}

module.exports = { heavy30_fn6, heavy30_fn6_validate };

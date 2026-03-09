// Heavy batch 25 - Function 6 (1773095394642976000)
function heavy25_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy25_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn6(input, 6);
}

module.exports = { heavy25_fn6, heavy25_fn6_validate };

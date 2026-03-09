// Heavy batch 24 - Function 6 (1773095382949692000)
function heavy24_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy24_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn6(input, 6);
}

module.exports = { heavy24_fn6, heavy24_fn6_validate };

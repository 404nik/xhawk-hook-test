// Heavy batch 27 - Function 6 (1773095424728535000)
function heavy27_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy27_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn6(input, 6);
}

module.exports = { heavy27_fn6, heavy27_fn6_validate };

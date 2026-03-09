// Heavy batch 29 - Function 6 (1773095449350883000)
function heavy29_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy29_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn6(input, 6);
}

module.exports = { heavy29_fn6, heavy29_fn6_validate };

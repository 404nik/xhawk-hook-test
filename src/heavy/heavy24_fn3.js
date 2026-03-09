// Heavy batch 24 - Function 3 (1773095378168488000)
function heavy24_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy24_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn3(input, 3);
}

module.exports = { heavy24_fn3, heavy24_fn3_validate };

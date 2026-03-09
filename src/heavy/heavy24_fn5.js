// Heavy batch 24 - Function 5 (1773095381323592000)
function heavy24_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy24_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn5(input, 5);
}

module.exports = { heavy24_fn5, heavy24_fn5_validate };

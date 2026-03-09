// Heavy batch 24 - Function 1 (1773095375039841000)
function heavy24_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy24_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn1(input, 1);
}

module.exports = { heavy24_fn1, heavy24_fn1_validate };

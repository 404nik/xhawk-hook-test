// Heavy batch 25 - Function 1 (1773095386136821000)
function heavy25_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy25_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn1(input, 1);
}

module.exports = { heavy25_fn1, heavy25_fn1_validate };

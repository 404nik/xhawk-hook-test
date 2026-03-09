// Heavy batch 25 - Function 7 (1773095396264915000)
function heavy25_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy25_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn7(input, 7);
}

module.exports = { heavy25_fn7, heavy25_fn7_validate };

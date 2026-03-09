// Heavy batch 25 - Function 5 (1773095392812040000)
function heavy25_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy25_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn5(input, 5);
}

module.exports = { heavy25_fn5, heavy25_fn5_validate };

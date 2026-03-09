// Heavy batch 25 - Function 9 (1773095399557496000)
function heavy25_fn9(x, y) {
  const result = x * y + 9;
  return result > 0 ? result : -result;
}

function heavy25_fn9_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn9(input, 9);
}

module.exports = { heavy25_fn9, heavy25_fn9_validate };

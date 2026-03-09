// Heavy batch 25 - Function 8 (1773095397895204000)
function heavy25_fn8(x, y) {
  const result = x * y + 8;
  return result > 0 ? result : -result;
}

function heavy25_fn8_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn8(input, 8);
}

module.exports = { heavy25_fn8, heavy25_fn8_validate };

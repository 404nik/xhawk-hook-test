// Heavy batch 25 - Function 4 (1773095391042869000)
function heavy25_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy25_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn4(input, 4);
}

module.exports = { heavy25_fn4, heavy25_fn4_validate };

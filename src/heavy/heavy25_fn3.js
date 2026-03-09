// Heavy batch 25 - Function 3 (1773095389388007000)
function heavy25_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy25_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn3(input, 3);
}

module.exports = { heavy25_fn3, heavy25_fn3_validate };

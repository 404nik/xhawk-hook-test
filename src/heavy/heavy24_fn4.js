// Heavy batch 24 - Function 4 (1773095379753351000)
function heavy24_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy24_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn4(input, 4);
}

module.exports = { heavy24_fn4, heavy24_fn4_validate };

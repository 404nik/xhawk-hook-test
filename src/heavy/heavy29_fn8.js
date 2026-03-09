// Heavy batch 29 - Function 8 (1773095452704717000)
function heavy29_fn8(x, y) {
  const result = x * y + 8;
  return result > 0 ? result : -result;
}

function heavy29_fn8_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn8(input, 8);
}

module.exports = { heavy29_fn8, heavy29_fn8_validate };

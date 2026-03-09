// Heavy batch 29 - Function 4 (1773095445929807000)
function heavy29_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy29_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn4(input, 4);
}

module.exports = { heavy29_fn4, heavy29_fn4_validate };

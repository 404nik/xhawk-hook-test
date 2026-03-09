// Heavy batch 27 - Function 4 (1773095421331406000)
function heavy27_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy27_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn4(input, 4);
}

module.exports = { heavy27_fn4, heavy27_fn4_validate };

// Heavy batch 27 - Function 7 (1773095426387357000)
function heavy27_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy27_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn7(input, 7);
}

module.exports = { heavy27_fn7, heavy27_fn7_validate };

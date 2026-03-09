// Heavy batch 24 - Function 7 (1773095384507183000)
function heavy24_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy24_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn7(input, 7);
}

module.exports = { heavy24_fn7, heavy24_fn7_validate };

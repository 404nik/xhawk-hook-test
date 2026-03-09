// Heavy batch 27 - Function 5 (1773095423091296000)
function heavy27_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy27_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn5(input, 5);
}

module.exports = { heavy27_fn5, heavy27_fn5_validate };

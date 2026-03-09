// Heavy batch 27 - Function 3 (1773095419672310000)
function heavy27_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy27_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn3(input, 3);
}

module.exports = { heavy27_fn3, heavy27_fn3_validate };

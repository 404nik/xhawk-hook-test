// Heavy batch 30 - Function 3 (1773095459491817000)
function heavy30_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy30_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn3(input, 3);
}

module.exports = { heavy30_fn3, heavy30_fn3_validate };

// Heavy batch 26 - Function 3 (1773095404717244000)
function heavy26_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy26_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn3(input, 3);
}

module.exports = { heavy26_fn3, heavy26_fn3_validate };

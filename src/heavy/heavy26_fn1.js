// Heavy batch 26 - Function 1 (1773095401216204000)
function heavy26_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy26_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn1(input, 1);
}

module.exports = { heavy26_fn1, heavy26_fn1_validate };

// Heavy batch 26 - Function 2 (1773095402993502000)
function heavy26_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy26_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn2(input, 2);
}

module.exports = { heavy26_fn2, heavy26_fn2_validate };

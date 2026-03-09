// Heavy batch 26 - Function 7 (1773095411382966000)
function heavy26_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy26_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn7(input, 7);
}

module.exports = { heavy26_fn7, heavy26_fn7_validate };

// Heavy batch 26 - Function 9 (1773095414575335000)
function heavy26_fn9(x, y) {
  const result = x * y + 9;
  return result > 0 ? result : -result;
}

function heavy26_fn9_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn9(input, 9);
}

module.exports = { heavy26_fn9, heavy26_fn9_validate };

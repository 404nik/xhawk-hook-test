// Heavy batch 26 - Function 4 (1773095406441364000)
function heavy26_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy26_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn4(input, 4);
}

module.exports = { heavy26_fn4, heavy26_fn4_validate };

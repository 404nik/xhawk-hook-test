// Heavy batch 26 - Function 6 (1773095409773899000)
function heavy26_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy26_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn6(input, 6);
}

module.exports = { heavy26_fn6, heavy26_fn6_validate };

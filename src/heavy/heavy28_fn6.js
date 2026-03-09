// Heavy batch 28 - Function 6 (1773095436922929000)
function heavy28_fn6(x, y) {
  const result = x * y + 6;
  return result > 0 ? result : -result;
}

function heavy28_fn6_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn6(input, 6);
}

module.exports = { heavy28_fn6, heavy28_fn6_validate };

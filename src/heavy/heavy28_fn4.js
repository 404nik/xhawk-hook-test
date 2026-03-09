// Heavy batch 28 - Function 4 (1773095433519358000)
function heavy28_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy28_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn4(input, 4);
}

module.exports = { heavy28_fn4, heavy28_fn4_validate };

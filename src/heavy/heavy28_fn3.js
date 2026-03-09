// Heavy batch 28 - Function 3 (1773095431501839000)
function heavy28_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy28_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn3(input, 3);
}

module.exports = { heavy28_fn3, heavy28_fn3_validate };

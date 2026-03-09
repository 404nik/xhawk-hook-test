// Heavy batch 28 - Function 1 (1773095428127662000)
function heavy28_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy28_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn1(input, 1);
}

module.exports = { heavy28_fn1, heavy28_fn1_validate };

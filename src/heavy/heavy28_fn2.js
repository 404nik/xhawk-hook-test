// Heavy batch 28 - Function 2 (1773095429750507000)
function heavy28_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy28_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn2(input, 2);
}

module.exports = { heavy28_fn2, heavy28_fn2_validate };

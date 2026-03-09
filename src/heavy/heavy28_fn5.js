// Heavy batch 28 - Function 5 (1773095435183604000)
function heavy28_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy28_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn5(input, 5);
}

module.exports = { heavy28_fn5, heavy28_fn5_validate };

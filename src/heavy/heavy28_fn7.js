// Heavy batch 28 - Function 7 (1773095438724049000)
function heavy28_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy28_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy28_fn7(input, 7);
}

module.exports = { heavy28_fn7, heavy28_fn7_validate };

// Heavy batch 27 - Function 1 (1773095416286755000)
function heavy27_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy27_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn1(input, 1);
}

module.exports = { heavy27_fn1, heavy27_fn1_validate };

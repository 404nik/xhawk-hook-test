// Heavy batch 24 - Function 2 (1773095376616862000)
function heavy24_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy24_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy24_fn2(input, 2);
}

module.exports = { heavy24_fn2, heavy24_fn2_validate };

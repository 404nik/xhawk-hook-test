// Heavy batch 27 - Function 2 (1773095417982401000)
function heavy27_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy27_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy27_fn2(input, 2);
}

module.exports = { heavy27_fn2, heavy27_fn2_validate };

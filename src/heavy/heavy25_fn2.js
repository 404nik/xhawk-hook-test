// Heavy batch 25 - Function 2 (1773095387743872000)
function heavy25_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy25_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy25_fn2(input, 2);
}

module.exports = { heavy25_fn2, heavy25_fn2_validate };

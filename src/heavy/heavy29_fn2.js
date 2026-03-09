// Heavy batch 29 - Function 2 (1773095442390734000)
function heavy29_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy29_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn2(input, 2);
}

module.exports = { heavy29_fn2, heavy29_fn2_validate };

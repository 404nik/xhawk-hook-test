// Heavy batch 29 - Function 1 (1773095440637633000)
function heavy29_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy29_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn1(input, 1);
}

module.exports = { heavy29_fn1, heavy29_fn1_validate };

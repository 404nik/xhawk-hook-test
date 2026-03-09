// Heavy batch 30 - Function 1 (1773095456146508000)
function heavy30_fn1(x, y) {
  const result = x * y + 1;
  return result > 0 ? result : -result;
}

function heavy30_fn1_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn1(input, 1);
}

module.exports = { heavy30_fn1, heavy30_fn1_validate };

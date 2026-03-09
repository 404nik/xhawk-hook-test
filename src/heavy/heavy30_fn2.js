// Heavy batch 30 - Function 2 (1773095457766828000)
function heavy30_fn2(x, y) {
  const result = x * y + 2;
  return result > 0 ? result : -result;
}

function heavy30_fn2_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn2(input, 2);
}

module.exports = { heavy30_fn2, heavy30_fn2_validate };

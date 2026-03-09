// Heavy batch 30 - Function 7 (1773095466193797000)
function heavy30_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy30_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn7(input, 7);
}

module.exports = { heavy30_fn7, heavy30_fn7_validate };

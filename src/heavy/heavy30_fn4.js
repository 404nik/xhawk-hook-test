// Heavy batch 30 - Function 4 (1773095461115282000)
function heavy30_fn4(x, y) {
  const result = x * y + 4;
  return result > 0 ? result : -result;
}

function heavy30_fn4_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn4(input, 4);
}

module.exports = { heavy30_fn4, heavy30_fn4_validate };

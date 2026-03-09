// Heavy batch 30 - Function 5 (1773095462864983000)
function heavy30_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy30_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy30_fn5(input, 5);
}

module.exports = { heavy30_fn5, heavy30_fn5_validate };

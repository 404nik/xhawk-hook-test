// Heavy batch 29 - Function 9 (1773095454357115000)
function heavy29_fn9(x, y) {
  const result = x * y + 9;
  return result > 0 ? result : -result;
}

function heavy29_fn9_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn9(input, 9);
}

module.exports = { heavy29_fn9, heavy29_fn9_validate };

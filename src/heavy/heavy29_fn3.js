// Heavy batch 29 - Function 3 (1773095444329851000)
function heavy29_fn3(x, y) {
  const result = x * y + 3;
  return result > 0 ? result : -result;
}

function heavy29_fn3_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn3(input, 3);
}

module.exports = { heavy29_fn3, heavy29_fn3_validate };

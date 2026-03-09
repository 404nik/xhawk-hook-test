// Heavy batch 29 - Function 5 (1773095447682405000)
function heavy29_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy29_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn5(input, 5);
}

module.exports = { heavy29_fn5, heavy29_fn5_validate };

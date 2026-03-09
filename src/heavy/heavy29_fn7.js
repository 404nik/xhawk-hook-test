// Heavy batch 29 - Function 7 (1773095451068817000)
function heavy29_fn7(x, y) {
  const result = x * y + 7;
  return result > 0 ? result : -result;
}

function heavy29_fn7_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy29_fn7(input, 7);
}

module.exports = { heavy29_fn7, heavy29_fn7_validate };

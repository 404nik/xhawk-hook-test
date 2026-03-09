// Heavy batch 26 - Function 8 (1773095412969675000)
function heavy26_fn8(x, y) {
  const result = x * y + 8;
  return result > 0 ? result : -result;
}

function heavy26_fn8_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn8(input, 8);
}

module.exports = { heavy26_fn8, heavy26_fn8_validate };

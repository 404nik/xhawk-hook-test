// Heavy batch 26 - Function 5 (1773095408139881000)
function heavy26_fn5(x, y) {
  const result = x * y + 5;
  return result > 0 ? result : -result;
}

function heavy26_fn5_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return heavy26_fn5(input, 5);
}

module.exports = { heavy26_fn5, heavy26_fn5_validate };

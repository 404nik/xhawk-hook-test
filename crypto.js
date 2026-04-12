// Caesar cipher encrypt/decrypt
function caesarEncrypt(text, shift) {
  shift = ((shift % 26) + 26) % 26;
  return text.replace(/[a-zA-Z]/g, (ch) => {
    const base = ch >= 'a' ? 97 : 65;
    return String.fromCharCode(((ch.charCodeAt(0) - base + shift) % 26) + base);
  });
}

function caesarDecrypt(text, shift) {
  return caesarEncrypt(text, 26 - shift);
}

// XOR cipher encrypt/decrypt (symmetric — same function for both)
function xorCipher(text, key) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
    result += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
  }
  return result;
}

// Base64 encode/decode
function base64Encode(text) {
  return Buffer.from(text, 'utf-8').toString('base64');
}

function base64Decode(encoded) {
  return Buffer.from(encoded, 'base64').toString('utf-8');
}

// ROT13 (special case of Caesar with shift=13, self-inverting)
function rot13(text) {
  return caesarEncrypt(text, 13);
}

module.exports = {
  caesarEncrypt,
  caesarDecrypt,
  xorCipher,
  base64Encode,
  base64Decode,
  rot13
};

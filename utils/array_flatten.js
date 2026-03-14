function flattenArray(arr) {
  return arr.reduce((acc, val) => {
    return Array.isArray(val) 
      ? acc.concat(flattenArray(val)) 
      : acc.concat(val);
  }, []);
}

module.exports = { flattenArray };

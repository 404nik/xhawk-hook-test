# Utils Directory

This directory contains utility modules used across the project.

## `alphabet_validator.js`

- **isAlphabetOnly(text)**: Returns `true` if `text` is a non-empty string containing only letters `a-z` or `A-Z`, otherwise `false`.

## `factorial_helper.js`

- **calculateFactorial(n)**: Computes the factorial of a non-negative integer `n`; returns `1` for `0`, and `0` for invalid inputs.

## `gemini_helper.py`

- **gemini_helper()**: Simple Python helper that returns a message `"Gemini is helping!"`.

## `math_utils.js`

- **clamp(value, min, max)**: Clamps `value` to be within the range `[min, max]`, swapping `min` and `max` if they are in the wrong order.
- **average(numbers)**: Returns the arithmetic mean of numeric values in the `numbers` array, or `NaN` for invalid or empty input.
- **isPrime(n)**: Returns `true` if `n` is an integer greater than `1` and prime, otherwise `false`.

## `object_merger.js`

- **mergeObjects(obj1, obj2)**: Returns a new object formed by shallow-merging the properties of `obj1` and `obj2` (properties from `obj2` override `obj1`).

## `string_utils.js`

- **truncateString(str, maxLength)**: Truncates `str` to `maxLength` characters and appends `"..."` when truncation occurs, with safe handling for edge cases.
- **capitalizeWords(str)**: Returns a new string with the first letter of each word capitalized and the rest lowercased.
- **countWords(str)**: Counts and returns the number of whitespace-separated words in `str`.
- **reverseString(str)**: Returns a new string with the characters of `str` in reverse order.


# xhawk-hook-test

## Overview

A collection of JavaScript utility functions for common operations including array manipulation, date handling, and basic arithmetic.

## Utils

### `utils/array_utils.js`

- **`flattenArray(arr)`** - Flattens a nested array one level deep.
- **`uniqueValues(arr)`** - Returns an array with duplicate values removed.
- **`chunkArray(arr, size)`** - Splits an array into chunks of the given size.
- **`groupBy(arr, keyFn)`** - Groups array elements into an object by the result of keyFn.

### `utils/date_utils.js`

- **`daysBetween(date1, date2)`** - Returns the number of days between two Date objects.
- **`isWeekend(date)`** - Returns true if the date falls on Saturday or Sunday.
- **`addDays(date, n)`** - Returns a new Date that is n days after the given date.

## Config

No configuration files are present at this time.

## Tests

### `sync_test.js`

Contains basic arithmetic functions (`add`, `subtract`, `multiply`, `divide`, `power`, `modulo`) used for testing purposes.

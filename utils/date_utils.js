function daysBetween(date1, date2) {
  const msPerDay = 1000 * 60 * 60 * 24;
  return Math.round(Math.abs(date2 - date1) / msPerDay);
}

function isWeekend(date) {
  const day = date.getDay();
  return day === 0 || day === 6;
}

function addDays(date, n) {
  const result = new Date(date);
  result.setDate(result.getDate() + n);
  return result;
}

module.exports = { daysBetween, isWeekend, addDays };

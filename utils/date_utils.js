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

function formatDate(date, format) {
  const yyyy = date.getFullYear().toString();
  const mm = (date.getMonth() + 1).toString().padStart(2, '0');
  const dd = date.getDate().toString().padStart(2, '0');
  return format.replace('YYYY', yyyy).replace('MM', mm).replace('DD', dd);
}

function startOfWeek(date) {
  const result = new Date(date);
  const day = result.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  result.setDate(result.getDate() + diff);
  return result;
}

module.exports = { daysBetween, isWeekend, addDays, formatDate, startOfWeek };

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3,
};

let currentLevel = LOG_LEVELS.DEBUG;

function setLevel(level) {
  currentLevel = LOG_LEVELS[level] ?? LOG_LEVELS.DEBUG;
}

function formatTimestamp() {
  return new Date().toISOString();
}

function log(level, message, data) {
  if (LOG_LEVELS[level] < currentLevel) return;

  const entry = {
    timestamp: formatTimestamp(),
    level,
    message,
    ...(data && { data }),
    pid: process.pid,
  };

  const output = JSON.stringify(entry);

  if (level === "ERROR") {
    console.error(output);
  } else if (level === "WARN") {
    console.warn(output);
  } else {
    console.log(output);
  }

  return entry;
}

function debug(message, data) { return log("DEBUG", message, data); }
function info(message, data) { return log("INFO", message, data); }
function warn(message, data) { return log("WARN", message, data); }
function error(message, data) { return log("ERROR", message, data); }

function requestLogger(req, res, next) {
  const start = Date.now();
  const { method, url, headers } = req;

  info("Incoming request", {
    method,
    url,
    userAgent: headers["user-agent"],
    ip: req.headers["x-forwarded-for"] || req.socket?.remoteAddress,
  });

  const originalEnd = res.end;
  res.end = function (...args) {
    const duration = Date.now() - start;
    info("Request completed", {
      method,
      url,
      statusCode: res.statusCode,
      durationMs: duration,
    });
    originalEnd.apply(res, args);
  };

  if (next) next();
}

function telemetry(event, metadata) {
  return info(`[TELEMETRY] ${event}`, {
    event,
    ...metadata,
    timestamp: formatTimestamp(),
  });
}

module.exports = {
  debug,
  info,
  warn,
  error,
  setLevel,
  requestLogger,
  telemetry,
  LOG_LEVELS,
};

"use strict";

const { RateLimiter } = require("./rate_limiter");

class RateLimiterDebugModule {
  constructor(options = {}) {
    this.limiter = options.limiter ?? new RateLimiter(options);
    this.maxLogEntries = Number(options.maxLogEntries ?? 1000);
    this.logs = [];
  }

  attempt(key = "global", cost = 1, meta = {}) {
    const decision = this.limiter.consume(key, cost);

    const entry = {
      timestamp: new Date().toISOString(),
      key: decision.key,
      cost: decision.cost,
      allowed: decision.allowed,
      remainingTokens: decision.remainingTokens,
      retryAfterMs: decision.retryAfterMs,
      reason: decision.allowed ? "tokens_available" : "rate_limited",
      meta,
    };

    this.logs.push(entry);
    if (this.logs.length > this.maxLogEntries) {
      this.logs.shift();
    }

    return entry;
  }

  getLogs(filters = {}) {
    const { key, allowed } = filters;
    return this.logs.filter((entry) => {
      if (typeof key === "string" && entry.key !== key) {
        return false;
      }
      if (typeof allowed === "boolean" && entry.allowed !== allowed) {
        return false;
      }
      return true;
    });
  }

  getSummary() {
    let allowed = 0;
    let blocked = 0;

    for (const entry of this.logs) {
      if (entry.allowed) {
        allowed += 1;
      } else {
        blocked += 1;
      }
    }

    return {
      total: this.logs.length,
      allowed,
      blocked,
    };
  }

  clearLogs() {
    this.logs = [];
  }
}

module.exports = {
  RateLimiterDebugModule,
};

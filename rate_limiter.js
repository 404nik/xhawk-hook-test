"use strict";

class RateLimiter {
  constructor(options = {}) {
    const capacity = Number(options.capacity ?? 10);
    const refillPerSecond = Number(options.refillPerSecond ?? 5);

    if (!Number.isFinite(capacity) || capacity <= 0) {
      throw new Error("capacity must be a positive number");
    }
    if (!Number.isFinite(refillPerSecond) || refillPerSecond <= 0) {
      throw new Error("refillPerSecond must be a positive number");
    }

    this.capacity = capacity;
    this.refillPerSecond = refillPerSecond;
    this.now = typeof options.now === "function" ? options.now : Date.now;
    this.buckets = new Map();
  }

  _roundTokens(tokens) {
    return Number(tokens.toFixed(3));
  }

  _getBucket(key) {
    if (!this.buckets.has(key)) {
      this.buckets.set(key, {
        tokens: this.capacity,
        lastRefillMs: this.now(),
      });
    }
    return this.buckets.get(key);
  }

  _refill(bucket, nowMs) {
    const elapsedMs = Math.max(0, nowMs - bucket.lastRefillMs);
    if (elapsedMs === 0) {
      return;
    }

    const refillAmount = (elapsedMs / 1000) * this.refillPerSecond;
    bucket.tokens = Math.min(this.capacity, bucket.tokens + refillAmount);
    bucket.lastRefillMs = nowMs;
  }

  getStatus(key = "global") {
    const nowMs = this.now();
    const bucket = this._getBucket(key);
    this._refill(bucket, nowMs);

    return {
      key,
      capacity: this.capacity,
      refillPerSecond: this.refillPerSecond,
      tokens: this._roundTokens(bucket.tokens),
      lastRefillMs: bucket.lastRefillMs,
    };
  }

  reset(key = "global") {
    this.buckets.delete(key);
  }

  consume(key = "global", cost = 1) {
    const nowMs = this.now();
    const safeCost = Number(cost);
    if (!Number.isFinite(safeCost) || safeCost <= 0) {
      throw new Error("cost must be a positive number");
    }

    const bucket = this._getBucket(key);
    this._refill(bucket, nowMs);

    if (bucket.tokens >= safeCost) {
      bucket.tokens -= safeCost;
      return {
        allowed: true,
        key,
        cost: safeCost,
        remainingTokens: this._roundTokens(bucket.tokens),
        retryAfterMs: 0,
      };
    }

    const missingTokens = safeCost - bucket.tokens;
    const retryAfterMs = Math.ceil((missingTokens / this.refillPerSecond) * 1000);

    return {
      allowed: false,
      key,
      cost: safeCost,
      remainingTokens: this._roundTokens(bucket.tokens),
      retryAfterMs,
    };
  }
}

module.exports = {
  RateLimiter,
};

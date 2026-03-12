/**
 * Simple rate limiter (design only — not wired to real timers/storage).
 * Token-bucket style: refill tokens over time, consume one per request.
 */

function createRateLimiter(options = {}) {
  const {
    maxTokens = 6,
    refillRatePerSecond = 6,
    keyFn = (id) => id,
  } = options;

  // In-memory store: key -> { tokens, lastRefillAt }
  const buckets = new Map();

  function getBucket(key) {
    const id = keyFn(key);
    if (!buckets.has(id)) {
      buckets.set(id, { tokens: maxTokens, lastRefillAt: Date.now() });
    }
    return buckets.get(id);
  }

  function refill(bucket) {
    const now = Date.now();
    const elapsed = (now - bucket.lastRefillAt) / 1000;
    const toAdd = Math.floor(elapsed * refillRatePerSecond);
    bucket.tokens = Math.min(maxTokens, bucket.tokens + toAdd);
    bucket.lastRefillAt = now;
  }

  return {
    /** Check if a request is allowed (consumes 1 token if allowed). */
    allow(key) {
      const bucket = getBucket(key);
      refill(bucket);
      if (bucket.tokens >= 1) {
        bucket.tokens -= 1;
        return { allowed: true, remaining: bucket.tokens };
      }
      return { allowed: false, remaining: 0 };
    },

    /** Check only — does not consume a token. */
    peek(key) {
      const bucket = getBucket(key);
      refill(bucket);
      return { allowed: bucket.tokens >= 1, remaining: bucket.tokens };
    },

    /** Reset limit for a key (e.g. for testing). */
    reset(key) {
      buckets.delete(keyFn(key));
    },
  };
}

module.exports = { createRateLimiter };

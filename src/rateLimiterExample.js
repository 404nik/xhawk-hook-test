/**
 * Example usage of the rate limiter (design demo).
 */

const { createRateLimiter } = require("./rateLimiter");

// 6 requests per second
const limiter = createRateLimiter({ maxTokens: 6, refillRatePerSecond: 6 });

// Simulate requests by key (e.g. user id or IP)
function tryRequest(userId) {
  const result = limiter.allow(userId);
  if (result.allowed) {
    console.log(`OK — user ${userId}, remaining: ${result.remaining}`);
  } else {
    console.log(`RATE LIMITED — user ${userId}`);
  }
  return result;
}

// Demo: burst then limit
["alice", "alice", "alice", "bob"].forEach((id) => tryRequest(id));
limiter.reset("alice"); // reset for next test

module.exports = { tryRequest, createRateLimiter };

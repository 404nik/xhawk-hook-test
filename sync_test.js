function add(a, b) {
  return a + b;
}

function gcd(a, b) {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b !== 0) {
    const t = b;
    b = a % b;
    a = t;
  }
  return a;
}

function isPrime(n) {
  n = Number(n);
  if (!Number.isFinite(n) || n < 2) return false;
  if (n % 2 === 0) return n === 2;
  const limit = Math.floor(Math.sqrt(n));
  for (let d = 3; d <= limit; d += 2) {
    if (n % d === 0) return false;
  }
  return true;
}

function factorial(n) {
  n = Number(n);
  if (!Number.isInteger(n) || n < 0) return null;
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}

function lcm(a, b) {
  if (a === 0 && b === 0) return 0;
  return Math.abs(a * b) / gcd(a, b);
}

function clamp(x, lo, hi) {
  return Math.min(hi, Math.max(lo, x));
}

function fibonacciModulo(n, mod) {
  n = Number(n);
  mod = Number(mod);
  if (!Number.isInteger(n) || n < 0) return null;
  if (!Number.isInteger(mod) || mod <= 0) return null;
  if (n === 0) return 0;
  if (n === 1) return 1 % mod;

  let prev = 0;
  let curr = 1 % mod;
  for (let i = 2; i <= n; i++) {
    const next = (prev + curr) % mod;
    prev = curr;
    curr = next;
  }
  return curr;
}

/** Population stdev by default; pass true for sample (Bessel) stdev. */
function standardDeviation(values, sample = false) {
  if (!Array.isArray(values) || values.length === 0) return null;
  const n = values.length;
  const mean = values.reduce((s, x) => s + Number(x), 0) / n;
  const divisor = sample ? (n > 1 ? n - 1 : 1) : n;
  const variance =
    values.reduce((s, x) => s + (Number(x) - mean) ** 2, 0) / divisor;
  return Math.sqrt(variance);
}

function makePseudoRandom(seed = 123456789) {
  // Deterministic PRNG for stable demo output.
  let s = seed >>> 0;
  return function next() {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    return s / 0x100000000;
  };
}

function formatSummary(summary) {
  const { total = 0, allowed = 0, blocked = 0 } = summary ?? {};
  const allowRate = total ? allowed / total : 0;
  const blockedRate = total ? blocked / total : 0;
  return {
    ...summary,
    total,
    allowed,
    blocked,
    allowRate,
    blockedRate,
  };
}

const { RateLimiterDebugModule } = require("./rate_limiter_debug");

function runRateLimiterDebugDemo() {
  const debugLimiter = new RateLimiterDebugModule({
    capacity: 3,
    refillPerSecond: 1,
    maxLogEntries: 50,
  });

  const nextRand = makePseudoRandom(1337);

  // Build a small deterministic list of prime keys.
  const primeKeys = [];
  for (let i = 2; primeKeys.length < 7; i++) {
    if (isPrime(i)) primeKeys.push(i);
  }

  const attempts = [];

  const pickPrime = () => primeKeys[Math.floor(nextRand() * primeKeys.length)];
  const pickCost = (p, q, i) => {
    const g = gcd(p, q);
    const base = g === 1 ? 2 : 1;
    const jitter = (i % 3) === 0 ? 1 : 0;
    const bursty = nextRand() > 0.85 ? 1 : 0;
    return base + jitter + bursty;
  };

  // Spread attempts across prime-pair keys.
  for (let i = 0; i < 16; i++) {
    const p = pickPrime();
    const q = pickPrime();
    const key = `pair:${p}x${q}`;
    const cost = pickCost(p, q, i);
    attempts.push(debugLimiter.attempt(key, cost, { i, p, q }));
  }

  // Add a hot key burst to force blocks (use repeated pair).
  const hotP = primeKeys[0];
  const hotQ = primeKeys[1];
  const hotKey = `pair:${hotP}x${hotQ}`;
  for (let burst = 0; burst < 6; burst++) {
    const cost = burst % 3 === 0 ? 3 : burst % 2 === 0 ? 2 : 1;
    attempts.push(debugLimiter.attempt(hotKey, cost, { burst, hotP, hotQ }));
  }

  const costs = attempts.map((a) => a.cost);

  return {
    attempts,
    summary: formatSummary(debugLimiter.getSummary()),
    meta: {
      hotKey,
      primeKeys,
      primePairHint: `${hotP}x${hotQ}`,
      costStdev: standardDeviation(costs),
    },
  };
}

if (require.main === module) {
  const demo = runRateLimiterDebugDemo();
  console.log("Rate limiter debug demo:");
  console.log(JSON.stringify(demo, null, 2));
}

module.exports = {
  add,
  gcd,
  isPrime,
  factorial,
  lcm,
  clamp,
  fibonacciModulo,
  standardDeviation,
  runRateLimiterDebugDemo,
};

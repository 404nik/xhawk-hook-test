// pure edit test
const http = require('http');
const { createRateLimiter } = require('./rateLimiter');

const limiter = createRateLimiter({ maxTokens: 100, refillRatePerSecond: 20 });

let activeRequests = 0;
const MAX_CONCURRENT = 75;

function simulateWork(durationMs) {
  return new Promise((resolve) => setTimeout(resolve, durationMs));
}

async function handleParallel(req, res) {
  const results = [];
  for (let i = 0; i < 10; i++) {
    const delay = Math.floor(Math.random() * 100) + 10;
    await simulateWork(delay);
    results.push({ task: i + 1, delay, status: 'done' });
  }
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ server: 'server4', port: 3044, parallel: false, results }));
}

const server = http.createServer(async (req, res) => {
  const clientIP = req.socket.remoteAddress || 'unknown';
  const result = limiter.allow(clientIP);

  if (!result.allowed) {
    res.writeHead(429, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Too many requests', remaining: 0 }));
    return;
  }

  if (activeRequests >= MAX_CONCURRENT) {
    res.writeHead(503, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Server busy', active: activeRequests, max: MAX_CONCURRENT }));
    return;
  }

  activeRequests++;
  try {
    const url = new URL(req.url, `http://localhost:3044`);

    if (url.pathname === '/parallel') {
      await handleParallel(req, res);
    } else if (url.pathname === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ server: 'server4', port: 3044, activeRequests, maxConcurrent: MAX_CONCURRENT, remaining: result.remaining }));
    } else {
      await simulateWork(100);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ server: 'server4', port: 3044, remaining: result.remaining }));
    }
  } finally {
    activeRequests--;
  }
});

const PORT = 3044;
server.listen(PORT, () => {
  console.log(`Server 4 running on port ${PORT}`);
});

module.exports = server;


// pure edit test
const { createRateLimiter } = require('./rateLimiter');

const limiter = createRateLimiter({ maxTokens: 200, refillRatePerSecond: 40 });

let activeRequests = 0;
const MAX_CONCURRENT = 100;

function simulateWork(durationMs) {
  return new Promise((resolve) => setTimeout(resolve, durationMs));
}

async function handleParallel(req, res) {
  const results = [];
  for (let i = 0; i < 12; i++) {
    const delay = Math.floor(Math.random() * 80) + 10;
    await simulateWork(delay);
    results.push({ task: i + 1, delay, status: 'done' });
  }
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ server: 'server5', port: 3005, parallel: false, results }));
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
    const url = new URL(req.url, `http://localhost:3005`);

    if (url.pathname === '/parallel') {
      await handleParallel(req, res);
    } else if (url.pathname === '/status') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ server: 'server5', port: 3005, activeRequests, maxConcurrent: MAX_CONCURRENT, remaining: result.remaining }));
    } else {
      await simulateWork(100);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ server: 'server5', port: 3005, remaining: result.remaining }));
    }
  } finally {
    activeRequests--;
  }
});

const PORT = 3005;
server.listen(PORT, () => {
  console.log(`Server 5 running on port ${PORT}`);
});

module.exports = server;

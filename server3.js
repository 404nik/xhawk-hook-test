const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Server 3');
});

server.listen(3003, () => {
  console.log('Server 3 running on port 3003');
});

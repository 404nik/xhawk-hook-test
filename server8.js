const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Updated Server 8');
});

server.listen(3008, () => {
  console.log('Updated Server 8 running on port 3008');
});

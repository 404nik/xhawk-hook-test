const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Server 6');
});

server.listen(3006, () => {
  console.log('Server 6 running on port 3006');
});

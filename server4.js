const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Server 4');
});

server.listen(3004, () => {
  console.log('Server 4 running on port 3004');
});

const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Server 7');
});

server.listen(3007, () => {
  console.log('Server 7 running on port 3007');
});

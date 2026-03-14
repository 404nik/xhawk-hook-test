const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello from Server 5');
});

server.listen(3005, () => {
  console.log('Server 5 running on port 3005');
});

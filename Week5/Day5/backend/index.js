const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end("Production stack working with Docker");
});

server.listen(3000, () => {
  console.log("Backend running on port 3000");
});
const http = require("http");

let count = 0; //count for memory

const server = http.createServer((req, res) => {
  //-->  /ping
  if (req.url === "/ping") {
    const time = Date.now();
    res.end(`pong ${time}`);
  }
  //-->  /headers
  else if (req.url === "/headers") {
    res.setHeader("Content-Type", "application/json");
    res.end(JSON.stringify(req.headers, null, 2));
  }
  //-->  /count
  else if (req.url === "/count") {
    count++;
    res.end(`count:${count}`);
  }

  // default
  else {
    res.statusCode = 404;
    res.end("Not found");
  }
});
server.listen(3000, () => {
  console.log("Server is running at http://localhost:3000");
});

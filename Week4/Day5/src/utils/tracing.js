const { randomUUID } = require("crypto");

function tracingMiddleware(req, res, next) {
  const requestId = randomUUID();
  req.requestId = requestId;
  res.setHeader("X-Request-ID", requestId);
  next();
}

module.exports = tracingMiddleware;
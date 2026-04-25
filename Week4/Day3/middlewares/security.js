const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const mongoSanitize = require("express-mongo-sanitize");
const hpp = require("hpp");

const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    message: "Too many requests",
    code: "RATE_LIMIT_EXCEEDED",
  },
});

const corsOptions = {
  origin: "*",
  methods: ["GET", "POST", "DELETE"],
};

module.exports = {
  helmetMiddleware: helmet(),
  corsMiddleware: cors(corsOptions),
  rateLimiter,
  mongoSanitizeMiddleware: mongoSanitize({
    replaceWith: "_"
  }),
  hppMiddleware: hpp(),
};
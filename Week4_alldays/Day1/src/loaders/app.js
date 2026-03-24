const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const connectDB = require("./db");
const mongoose = require("mongoose");
const fs = require("fs");
const path = require("path");

const {
  helmetMiddleware,
  corsMiddleware,
  rateLimiter,
  mongoSanitizeMiddleware,
  hppMiddleware,
} = require("../middlewares/security");

const sanitizeMiddleware = require("../middlewares/sanitize.middleware");
const errorMiddleware = require("../middlewares/error.middleware");
const tracingMiddleware = require("../utils/tracing");

//request logger here
function requestLogger(req, res, next) {
  logger.info({
    requestId: req.requestId,
    method: req.method,
    url: req.originalUrl,
  });
  next();
}

//auto route loader
function loadRoutes(app) {
  const routesPath = path.join(__dirname, "../routes");
  const files = fs.readdirSync(routesPath);

  let routeCount = 0;

  files.forEach((file) => {
    const route = require(`../routes/${file}`);
    const routeName = file.replace(".routes.js", "");

    app.use(`/${routeName}`, route);
    routeCount++;
  });

  return routeCount;
}

async function startServer() {
  const app = express();

  app.use(tracingMiddleware);
  app.use(requestLogger);
//security 
  app.use(helmetMiddleware);
  app.use(corsMiddleware);
  app.use(rateLimiter);
  app.use(mongoSanitizeMiddleware);
  app.use(hppMiddleware);
  

//body parser
  app.use(express.json({ limit: "10kb" }));
  app.use(sanitizeMiddleware);

  logger.info("Middlewares loaded");

  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  const routeCount = loadRoutes(app);
  logger.info(`Routes mounted: ${routeCount}`);

  app.use(errorMiddleware);

  try {
    await connectDB();
    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed");
    process.exit(1);
  }

  const server = app.listen(config.port, () => {
    console.log(`Server running on ${config.port}`);
    logger.info(`Server started on port ${config.port}`);
  });

//-->graceful shutdown
  const shutdown = async () => {
    try {
      console.log("Graceful shutdown started");
      logger.info("Graceful shutdown started");

      await mongoose.connection.close();

      server.close(() => {
        console.log("Server closed");
        logger.info("Server closed");
        process.exit(0);
      });
    } catch (err) {
      console.error("Shutdown error:", err);
      process.exit(1);
    }
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
}

module.exports = startServer;
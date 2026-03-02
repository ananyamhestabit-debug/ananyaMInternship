const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const connectDB = require("./db");
const mongoose = require("mongoose");

const {
  helmetMiddleware,
  corsMiddleware,
  rateLimiter,
  mongoSanitizeMiddleware,
  hppMiddleware
} = require("../middlewares/security");

const { validateProduct } = require("../middlewares/validate");
const productController = require("../controllers/product.controller");
const errorMiddleware = require("../middlewares/error.middleware");
const tracingMiddleware = require("../utils/tracing");

async function startServer() {
  const app = express();

  app.use(tracingMiddleware);
  app.use(helmetMiddleware);
  app.use(corsMiddleware);
  app.use(rateLimiter);
  app.use(mongoSanitizeMiddleware);
  app.use(hppMiddleware);
  app.use(express.json({ limit: "10kb" }));

  logger.info("Security middlewares loaded");

  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  const productRoutes = require("../routes/product.routes");

  app.use("/products", productRoutes);

  logger.info("Routes mounted");

  app.use(errorMiddleware);

  await connectDB();

  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });

  process.on("SIGINT", async () => {
    logger.info("Graceful shutdown started");
    await mongoose.connection.close();
    server.close(() => {
      logger.info("Server closed");
      process.exit(0);
    });
  });
}

module.exports = startServer;
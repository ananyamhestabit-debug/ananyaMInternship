const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const connectDB = require("./db");
const mongoose = require("mongoose");

async function startServer() {
  const app = express();

  app.use(express.json());
  logger.info("Middlewares loaded");

  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  logger.info("Routes mounted: 1 endpoint");

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
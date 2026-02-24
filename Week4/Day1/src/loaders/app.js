const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const connectDB = require("./db");
const mongoose = require("mongoose");

// Day 2 Repositories
const AccountRepository = require("../repositories/account.repository");
const OrderRepository = require("../repositories/order.repository");

async function startServer() {
  const app = express();

  // Middleware
  app.use(express.json());
  logger.info("Middlewares loaded");

  // Health Check Route
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  // -----------------------------
  // DAY 2 TEST ROUTES
  // -----------------------------

  // Create Account
  app.get("/create-account", async (req, res) => {
    try {
      const account = await AccountRepository.create({
        firstName: "Ananya",
        lastName: "Mishra",
        email: "ananya" + Date.now() + "@example.com",
        password: "123456",
      });

      res.json(account);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Get Paginated Accounts
  app.get("/accounts", async (req, res) => {
    try {
      const accounts = await AccountRepository.findPaginated(1, 5);
      res.json(accounts);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  // Create Order (requires accountId)
  app.get("/create-order/:accountId", async (req, res) => {
    try {
      const order = await OrderRepository.create({
        account: req.params.accountId,
        productName: "Laptop",
        amount: 50000,
        expiresAt: new Date(Date.now() + 60000), // 1 minute TTL
      });

      res.json(order);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  logger.info("Routes mounted");

  // Connect Database
  await connectDB();

  // Start Server
  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });

  // Graceful Shutdown
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
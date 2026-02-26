const express = require("express");
const config = require("../config");
const logger = require("../utils/logger");
const connectDB = require("./db");
const mongoose = require("mongoose");

// Day 2 Repositories
const AccountRepository = require("../repositories/account.repository");
const OrderRepository = require("../repositories/order.repository");

// Day 3 Controller + Error Middleware
const productController = require("../controllers/product.controller");
const errorMiddleware = require("../middlewares/error.middleware");

async function startServer() {
  const app = express();


  // GLOBAL MIDDLEWARES
  app.use(express.json());
  logger.info("Middlewares loaded");

  // HEALTH CHECK
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  // DAY 2 TEST ROUTES
  app.get("/create-account", async (req, res, next) => {
    try {
      const account = await AccountRepository.create({
        firstName: "Ananya",
        lastName: "Mishra",
        email: "ananya" + Date.now() + "@example.com",
        password: "123456",
      });

      res.json(account);
    } catch (error) {
      next(error);
    }
  });

  app.get("/accounts", async (req, res, next) => {
    try {
      const accounts = await AccountRepository.findPaginated(1, 5);
      res.json(accounts);
    } catch (error) {
      next(error);
    }
  });

  app.get("/create-order/:accountId", async (req, res, next) => {
    try {
      const order = await OrderRepository.create({
        account: req.params.accountId,
        productName: "Laptop",
        amount: 50000,
        expiresAt: new Date(Date.now() + 60000),
      });

      res.json(order);
    } catch (error) {
      next(error);
    }
  });


  // DAY 3 PRODUCT ROUTES
  app.get("/products", productController.getProducts);

  app.delete("/products/:id", productController.deleteProduct);

  logger.info("Routes mounted");

  // ERROR MIDDLEWARE (ALWAYS LAST)
  app.use(errorMiddleware);


  // DATABASE CONNECTION
  await connectDB();

  // SERVER START
  const server = app.listen(config.port, () => {
    logger.info(`Server started on port ${config.port}`);
  });

  // GRACEFUL SHUTDOWN
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
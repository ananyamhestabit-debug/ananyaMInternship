const mongoose = require("mongoose");
const config = require("../config");
const logger = require("../utils/logger");

async function connectDB() {
  try {
    await mongoose.connect(config.databaseUrl);
    logger.info("Database connected");
  } catch (error) {
    logger.error("Database connection failed");
    logger.error(error.message); 
    process.exit(1);
  }
}

module.exports = connectDB;
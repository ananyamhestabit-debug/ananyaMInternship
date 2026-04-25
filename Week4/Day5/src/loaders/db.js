const mongoose = require("mongoose");
const config = require("../config");
const logger = require("../utils/logger");

async function connectDB() {
  try {
    logger.info("Connecting to DB...");

    await mongoose.connect(config.databaseUrl);

    logger.info("DB Connected");
  } catch (err) {
    logger.error("DB Error:", err.message);
    process.exit(1);
  }
}

module.exports = connectDB;
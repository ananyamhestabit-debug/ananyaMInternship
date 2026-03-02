const mongoose = require("mongoose");
const config = require("../config");

async function connectDB() {
  try {
    console.log("CONNECTING TO DB:", config.databaseUrl);
    await mongoose.connect(config.databaseUrl, {
      serverSelectionTimeoutMS: 5000
    });
    console.log("DATABASE CONNECTED");
  } catch (error) {
    console.error("DB ERROR:", error.message);
  }
}

module.exports = connectDB;
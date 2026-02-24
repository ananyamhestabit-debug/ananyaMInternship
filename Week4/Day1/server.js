process.env.NODE_ENV = process.env.NODE_ENV || "local";

const startServer = require("./src/loaders/app");

startServer();
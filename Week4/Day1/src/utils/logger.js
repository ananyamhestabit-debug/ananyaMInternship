const pino = require("pino");
const fs = require("fs");
const path = require("path");

const logDir = path.join(__dirname, "../../logs");

if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir);
}

const logger = pino(
  {
    level: "info",
  },
  pino.destination(path.join(logDir, "app.log"))
);

module.exports = logger;
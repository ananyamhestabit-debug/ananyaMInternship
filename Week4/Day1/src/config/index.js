const path = require("path");
const dotenv = require("dotenv");

const env = process.env.NODE_ENV || "local";

const envFile = `.env.${env}`;

dotenv.config({
  path: path.resolve(process.cwd(), envFile),
});

module.exports = {
  port: process.env.PORT,
  databaseUrl: process.env.DATABASE_URL,
  nodeEnv: process.env.NODE_ENV,
};
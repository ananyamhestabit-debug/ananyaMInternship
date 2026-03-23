const path = require("path");
const dotenv = require("dotenv");

const env = process.env.NODE_ENV || "local";
const envFile = `.env.${env}`;

const result = dotenv.config({
  path: path.resolve(process.cwd(), envFile),
});

if (result.error) {
  console.warn(`Could not load ${envFile}`);
}

const requiredEnv = ["DATABASE_URL", "JWT_SECRET"];

requiredEnv.forEach((key) => {
  if (!process.env[key]) {
    throw new Error(`Missing env variable: ${key}`);
  }
});

module.exports = {
  port: process.env.PORT || 4000,
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || "1d",
  nodeEnv: env,
};
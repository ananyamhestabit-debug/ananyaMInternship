const { Worker } = require("bullmq");
const IORedis = require("ioredis");

const connection = new IORedis({
  maxRetriesPerRequest: null
});

console.log("Email worker started...");

const worker = new Worker(
  "emailQueue",
  async (job) => {
    console.log("Processing email for:", job.data.email);

    await new Promise(resolve => setTimeout(resolve, 2000));

    console.log("Email sent successfully to:", job.data.email);
  },
  { connection }
);

worker.on("failed", (job, err) => {
  console.error("Job failed:", err.message);
});
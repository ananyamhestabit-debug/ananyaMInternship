const { Queue } = require("bullmq");
const IORedis = require("ioredis");

const connection = new IORedis({
  maxRetriesPerRequest: null
});

const emailQueue = new Queue("emailQueue", {
  connection,
});

async function sendEmailJob(data) {
  await emailQueue.add("sendEmail", data, {
    attempts: 3,
    backoff: {
      type: "exponential", 
      delay: 2000,
    },
    removeOnComplete: true,
  });
}

module.exports = { sendEmailJob };
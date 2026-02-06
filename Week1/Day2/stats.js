const fs = require("fs");
const path = require("path");

// Clean up terminal inputs
const args = process.argv.slice(2);

// Group flags and files into pairs for processing
const jobList = [];
for (let i = 0; i < args.length; i += 2) {
  if (args[i] && args[i + 1]) {
    jobList.push({ mode: args[i], targetFile: args[i + 1] });
  }
}

// Stop if no valid file pairs are found
if (jobList.length === 0) {
  console.log("Usage: node stats.js --lines f1.txt --words f2.txt");
  process.exit();
}

// Ensure folders are ready before saving any data
if (!fs.existsSync("logs")) fs.mkdirSync("logs");
if (!fs.existsSync("output")) fs.mkdirSync("output");

function processFile({ mode, targetFile }) {
  return new Promise((resolve) => {
    if (!fs.existsSync(targetFile)) {
      console.log("Skipping missing file:", targetFile);
      return resolve(null);
    }

    // Start a high precision timer in nanoseconds
    const start = process.hrtime.bigint();

    fs.readFile(targetFile, "utf8", (err, content) => {
      if (err) {
        console.log("Could not read:", targetFile);
        return resolve(null);
      }

      // Check which count the user wants
      let result = 0;
      if (mode === "--chars") result = content.length;
      else if (mode === "--lines") result = content.split("\n").length;
      else if (mode === "--words") result = content.trim().split(/\s+/).length;

      // Bonus: remove duplicate lines and save separately
      const lines = content.split("\n");
      const uniqueData = [...new Set(lines)].join("\n");

      // FIXED: Using a fixed name so it overwrites instead of creating new ones
      const outPath = path.join(
        "output",
        `unique-${path.basename(targetFile)}`,
      );
      fs.writeFileSync(outPath, uniqueData);

      // Stop timer and convert to milliseconds
      const end = process.hrtime.bigint();
      const timeTaken = Number(end - start) / 1_000_000;

      // Measure memory usage in Megabytes
      const ramUsed = (process.memoryUsage().heapUsed / 1024 / 1024).toFixed(2);

      console.log(`${targetFile} [${mode.replace("--", "")}] -> ${result}`);

      // Return a report object to bundle everything together
      resolve({
        file: targetFile,
        executionTimeMs: timeTaken,
        memoryMB: ramUsed,
      });
    });
  });
}

// Process all files at the same time
const allPromises = jobList.map((item) => processFile(item));

Promise.all(allPromises).then((results) => {
  const cleanReports = results.filter((r) => r !== null);

  // FIXED: Removed Date.now() so the performance log overwrites itself
  const logPath = path.join("logs", "performance-report.json");
  fs.writeFileSync(logPath, JSON.stringify(cleanReports, null, 2));

  console.log(`\nDone! Final log updated at: ${logPath}`);
});

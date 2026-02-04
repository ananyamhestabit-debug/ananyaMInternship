# ananyaMInternship
# Engineering Mindset Bootcamp Assignments

This repository contains my assignments completed during the Engineering Mindset Bootcamp.
All work is organized week-wise and day-wise.
---
## Week 1 – Engineering Mindset & Node.js Basics
### Day 1 – System Reverse Engineering

**Objective:**
Understand the system environment using Node.js and Linux commands.

**Tasks Completed:**
- Created a Node.js script(sysinfo.js) to fetch system information.
- Displayed hostname, disk space, open ports, network gateway and logged-in users.
- Collected runtime metrics using Node.js process APIs.
- Stored system metrics in a JSON log file(day1-sysmetrics.json)

**Key Concepts Learned:**
- OS module in Node.js
- process API (cpuUsage, resourceUsage)
- Executing shell commands from Node.js
- Basic Linux commands and terminal usage

### Proof of Work (Deliverables)
#### Script (`sysinfo.js`) and Terminal Output
<img width="1447" height="1022" alt="Screenshot from 2026-02-03 17-23-49" src="https://github.com/user-attachments/assets/01583611-8a09-4751-810a-75bfca3c38f2" />


***

<img width="825" height="956" alt="week1day11" src="https://github.com/user-attachments/assets/e7c42193-55b8-4dc4-b84e-a144f3aba42b" />

---

#### logs/day1-sysmetrics.json
<img width="857" height="751" alt="week1day13" src="https://github.com/user-attachments/assets/049ab64c-10ab-4d76-8eb7-ea9ea897b6f0" />

---
###  .bashrc snippet screenshot
<img width="857" height="751" alt="week1day13" src="https://github.com/user-attachments/assets/3151ee86-3e6b-4742-a95d-95f6ad6eeda0" />

---

### Day 2 – Node CLI & File Processing

**Objective:**
Build a command-line tool using Node.js to analyze text files and process multiple files concurrently.

**Tasks Completed:**
- Developed a CLI tool (stats.js) using Node.js
- Counted total lines, words, and characters in text files
- Processed multiple files in parallel using asynchronous operations
- Measured execution time and memory usage for each file
- Generated performance logs in JSON format
- Removed duplicate lines and saved unique content to output files
- Created logs and output folders for structured results
- Added .gitignore to exclude generated files from version control

**Key Concepts Learned:**
- Node.js File System (fs / fs.promises)
- Command-line arguments (process.argv)
- Asynchronous programming
- Promise.all for concurrency
- Performance measurement (time and memory usage)
- Basic project structure and logging

### Proof of Work (Deliverables)

#### Script (`stats.js`) and Terminal Output
<img width="623" height="958" alt="image" src="https://github.com/user-attachments/assets/48f0544f-40e6-4840-b5f5-2eedd7e4bfbf" />

<img width="667" height="556" alt="image" src="https://github.com/user-attachments/assets/4647f96b-46d5-45eb-8f78-6b6c0c0c31da" />


---

#### Performance Logs (`logs/performance-*.json`)
<img width="722" height="552" alt="image" src="https://github.com/user-attachments/assets/7942d85a-f6b5-49e2-8edc-c3bc86ff3eca" />

---

#### Unique Output Files (`output/unique-*.txt`)
<img width="722" height="552" alt="image" src="https://github.com/user-attachments/assets/2323f2c9-72fa-4405-8612-735379e19852" />

---

**Usage:**

```bash
node stats.js --lines data1.txt
node stats.js --words data1.txt
node stats.js --chars data1.txt
node stats.js --unique data1.txt





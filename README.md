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


---

### Day 2 – Node CLI & File Processing

**Objective:**
Build a command-line tool to analyze text files using Node.js.

**Tasks Completed:**
- Created a CLI tool using Node.js
- Counted total lines, words and characters in text files
- Measured execution time and memory usage
- Generated performance logs in JSON format
- Removed duplicate lines and saved unique output to a file

**Usage:**
```bash
node stats.js --lines data1.txt
node stats.js --words data1.txt
node stats.js --chars data1.txt





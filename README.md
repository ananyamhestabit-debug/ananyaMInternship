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

---

<img width="825" height="956" alt="week1day11" src="https://github.com/user-attachments/assets/e7c42193-55b8-4dc4-b84e-a144f3aba42b" />

---

#### logs/day1-sysmetrics.json

<img width="857" height="751" alt="week1day13" src="https://github.com/user-attachments/assets/049ab64c-10ab-4d76-8eb7-ea9ea897b6f0" />

---

### .bashrc snippet screenshot

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

### Day 3 – Git Debugging & Release Workflow

**Objective:**
Learn advanced Git techniques to identify bugs and manage a stable release.

**Tasks Completed:**

- Created multiple commits to simulate versions
- Introduced a bug intentionally
- Used `git bisect` to locate the faulty commit
- Saved bisect logs as proof
- Created a release branch
- Used `git cherry-pick` to move only safe commits
- Used `git stash` for temporary changes

**Key Concepts Learned:**

- git bisect
- git cherry-pick
- git stash
- branching & release workflow

### Proof of Work (Deliverables)

#### Commit Graph Screenshot:

<img width="748" height="578" alt="commit graph week1-day3" src="https://github.com/user-attachments/assets/b43ef677-0dfc-4435-b590-c35b9cc92f99" />


---
<<<<<<< HEAD

## Day 4 – HTTP / API Forensics (cURL + Postman)

### Objective
Understand HTTP requests, inspect API headers, implement pagination, test APIs using Postman, and build a basic HTTP server with Node.js.

---

### Tasks Completed

- Fetched GitHub API data using cURL
- Captured verbose HTTP headers
- Extracted Rate-limit, ETag, and Server information
- Implemented pagination using `page` and `per_page=3`
- Retrieved 3 pages of repository data
- Documented Link headers and page navigation
- Created Postman collection for testing APIs
- Added Bearer token authentication
- Built a simple Node.js HTTP server

---

### Key Concepts Learned

- HTTP request/response cycle
- Headers analysis
- Rate limiting
- Pagination handling
- API testing with Postman
- Node.js HTTP server basics

---

### Server Endpoints Implemented

- `/ping` → returns current timestamp
- `/headers` → returns request headers
- `/count` → maintains in-memory request counter

---

# Day 5 – Automation & Mini CI Pipeline

## Objective
Learn basic automation and set up small CI checks to keep the project reliable and production ready.

---

## What I Built

- healthcheck.sh script to ping the server every 10 seconds  
- Logs failures automatically into logs/health.log  
- Husky pre-commit hook for validations  
- Blocks committing .env files  
- Blocks committing .log files  
- Runs Prettier to auto-format JavaScript  
- Creates bundle-<timestamp>.zip for packaging  
- Generates checksums.sha1 for integrity  
- Cron job to run healthcheck regularly  

---

## Project Files

- healthcheck.sh  
- .husky/pre-commit  
- logs/health.log  
- bundle-<timestamp>.zip  
- checksums.sha1  

---

## Key Concepts Learned

- Bash scripting  
- Automation and monitoring  
- Continuous integration basics  
- Pre-commit hooks  
- Code formatting  
- Packaging and checksums  
- Cron scheduling  

---

## Deliverables / Screenshots

Pre-commit Hook (fail):
<img width="1422" height="575" alt="pre commit fail" src="https://github.com/user-attachments/assets/1d21ba6f-5c8a-47f2-8a28-8bdbfac888e5" />



Pre-commit Hook (pass):
<img width="887" height="642" alt="husky pre commit hook ss" src="https://github.com/user-attachments/assets/855ae61f-9a20-46eb-8c7a-dc3741645167" />



Scheduled cron jobs:


<img width="676" height="280" alt="cron job scheduling" src="https://github.com/user-attachments/assets/c22880a0-cc58-4377-8e90-b9d9af979c36" />







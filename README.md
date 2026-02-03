# ananyaMInternship
# 🚀 Internship Learning Journey - Week 1

This repository documents my daily tasks, learnings, and engineering experiments during my internship.

---

## 🟦 Day 1: System Reverse Engineering & Node.js Basics

### 🎯 Goal
To understand how a high-level language like Node.js interacts with the Linux Operating System to fetch low-level hardware and network information.

### 🛠️ Tasks Performed
1. **System Health Script (`sysinfo.js`)**: 
   - Built a Node.js tool using `child_process` and `os` modules.
   - Fetched Hostname, Available Disk Space, Open Ports, Default Gateway, and Logged-in Users.
2. **Performance Logging**: 
   - Integrated `process.cpuUsage()` and `process.resourceUsage()` to monitor script efficiency.
   - Outputs are saved in JSON format under `/logs`.
3. **Terminal Optimization**:
   - Configured custom shell aliases in `.bashrc` to speed up common workflows:
     - `gs` -> `git status`
     - `files` -> `ls -lha`
     - `ports` -> Check listening network ports.

### 🧠 Key Learnings (The "Why")
- **Observability:** Learned that monitoring system metrics is crucial for server health.
- **Automation:** Understanding how scripts can replace manual terminal commands.
- **Data Serialization:** Learned why JSON is the standard for storing log data.

### 📂 Deliverables
- [x] `Week1/Day1/sysinfo.js`
- [x] `Week1/Day1/logs/day1-sysmetrics.json`

---

## 🟩 Day 2: Node.js CLI & Concurrency (In Progress)
- [ ] Building a file-processing CLI tool.
- [ ] Implementing Parallel Processing with `Promise.all()`.
- [ ] Memory and Execution time benchmarking.


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

### 📸 Proof of Work (Deliverables)

#### Script (`sysinfo.js`) and Terminal Output
<img width="1447" height="1022" alt="Screenshot from 2026-02-03 17-23-49" src="https://github.com/user-attachments/assets/01583611-8a09-4751-810a-75bfca3c38f2" />

<img width="825" height="956" alt="week1day11" src="https://github.com/user-attachments/assets/e7c42193-55b8-4dc4-b84e-a144f3aba42b" />


 
#### logs/day1-sysmetrics.json
<img width="857" height="751" alt="week1day13" src="https://github.com/user-attachments/assets/049ab64c-10ab-4d76-8eb7-ea9ea897b6f0" />


###  .bashrc snippet screenshot
<img width="857" height="751" alt="week1day13" src="https://github.com/user-attachments/assets/3151ee86-3e6b-4742-a95d-95f6ad6eeda0" />




---

## 🟩 Day 2: Node.js CLI & Concurrency (In Progress)
- [ ] Building a file-processing CLI tool.
- [ ] Implementing Parallel Processing with `Promise.all()`.
- [ ] Memory and Execution time benchmarking.


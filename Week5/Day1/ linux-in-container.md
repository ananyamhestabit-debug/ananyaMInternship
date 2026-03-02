# Linux Inside Docker Container

## 1. Container Entry
Used:
docker exec -it <container_id> /bin/sh

## 2. Directory Structure
Used ls command.
Observed /app directory containing project files.

## 3. Running Processes
Used ps and top.
Observed node process running.

## 4. Current User
Used whoami.
Observed container running as root.

## 5. Disk Usage
Used df -h.
Observed minimal Linux file system.

## 6. Logs
Used docker logs <container_id>.
Observed server startup message.

## 7. Observations
Container is isolated.
Node app runs inside Linux-based environment.
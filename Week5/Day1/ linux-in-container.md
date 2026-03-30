# Linux Inside Docker Container

## 1. Entering the Container

To access the running container (similar to SSH), the following command was used:

docker exec -it <container_id> /bin/sh

This opened a shell inside the container.


## 2. Exploring File System

### Command:
ls

### Purpose:
Lists all files and directories inside the container.

### Observation:
- Application files like index.js and package.json were present.
- The working directory was /app as defined in Dockerfile.

## 3. Checking Running Processes

### Command:
ps

### Purpose:
Shows running processes inside the container.

### Observation:
- Node.js process was running.
- This confirmed that our application is active inside the container.


## 4. Monitoring System Resources

### Command:
top

### Purpose:
Displays CPU and memory usage in real time.

### Observation:
- Node process was consuming resources.
- Container behaves like a small Linux system.

## 5. Checking Disk Usage

### Command:
df -h

### Purpose:
Shows disk usage in human-readable format.

### Observation:
- Container has its own isolated storage.
- Storage is limited compared to host system.

## 6. Viewing Logs

### Command (from host machine):
docker logs <container_id>

### Purpose:
Displays output logs of the container.

### Observation:
- Logs showed: "Server running on port 3000"
- Confirms application is running successfully.


## 7. Understanding Container Environment

### Users & Permissions

### Command:
whoami

### Observation:
- Default user inside container is root.


## 8. Key Learnings

- Containers have their own isolated file system.
- Each container runs its own processes.
- Logs help debug applications.
- Containers behave like lightweight Linux machines.
- Docker allows interacting with container OS using standard Linux commands.

<<------------------------------------------>
Commands-->
## 1. Building Docker Image

### Command:
docker build -t day1-app .

### Explanation:
- docker build → builds a Docker image
- -t day1-app → assigns a name to the image
- . --> current directory (where Dockerfile is present)

### Result:
A Docker image named "day1-app" is created.


## 2. Running the Container
### Command:
docker run -d -p 3001:3000 --name day1-container day1-app

### Explanation:
- docker run → starts a container
- -d -> runs container in background
- -p 3001:3000 → maps port 3001 (host) to 3000 (container)
- --name-> assigns a name to the container
- day1-app -> image name

### Result:
Container runs in background and application becomes accessible.

## 3. Accessing Application
Open browser:

http://localhost:3001

### Output:
Hello from Docker Container


## 4. Checking Running Containers
### Command:
docker ps

### Purpose:
Lists all running containers.

## 5. Entering the Container
### Command:
docker exec -it day1-container /bin/sh

### Explanation:
- docker exec → runs command inside container
- -it -> interactive terminal
- /bin/sh → opens shell

### Result:
Access to container's internal Linux environment.

## 6. Exploring Linux Inside Container
### List Files
Command:
ls

Purpose:
Displays files inside container.

### Check Running Processes
Command:
ps

Purpose:
Shows active processes.

Observation:
Node.js process is running.


### Monitor System Usage
Command:
top

Purpose:
Shows CPU and memory usage.

### Disk Usage
Command:
df -h

Purpose:
Shows disk usage in readable format.

### Folder Size
Command:
du -h

Purpose:
Shows size of files and folders.


### Check User
Command:
whoami

Purpose:
Displays current user inside container.

Observation:
Default user is root.

## 7. Viewing Logs

### Command:
docker logs day1-container

### Purpose:
Displays output logs of the container.

### Observation:
Server running message is shown.

## 8. Stopping and Removing Container

### Commands:
docker stop day1-container
docker rm day1-container

### Purpose:
Stops and deletes container.

## 9. Data Flow

Browser → localhost:3001  
 | 
Docker Port Mapping  
 |
Container (port 3000)  
 |
Node.js Server  
 |
Response → Hello from Docker Container


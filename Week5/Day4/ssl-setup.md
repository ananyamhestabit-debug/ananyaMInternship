# SSL Setup Documentation — Day 4

## Overview
This setup demonstrates enabling HTTPS for a Docker-based application using NGINX and self-signed SSL certificates generated using mkcert.

NGINX acts as a reverse proxy and handles HTTPS traffic.


## Step 1 — Add Local Domain
### Command:
sudo nano /etc/hosts

### Add this line:
127.0.0.1 app.local (Computer ko batana:
"jab bhi koi app.local bole → usse mere hi laptop pe bhej dena")

127.0.0.1   app.local
│            │
│            └── naam (domain)
└── IP address (localhost)

### Purpose:
Maps app.local to local machine (localhost)

## Step 2 — Verify Domain

### Command:
ping app.local

### Output:
64 bytes from app.local (127.0.0.1)

### Meaning:
Domain is correctly mapped

## Step 3 — Generate SSL Certificates

### Command:
mkcert app.local

### Output:
- app.local.pem
- app.local-key.pem

### Purpose:
Creates SSL certificate and private key for HTTPS

## Step 4 — Move Certificates

### Commands:
mkdir certs
mv app.local.pem certs/
mv app.local-key.pem certs/

(If permission issue)
sudo mv app.local.pem certs/
sudo mv app.local-key.pem certs/


## Step 5 — Start Docker Containers

### Command:
docker compose up -d

### Output:
Containers created:
- backend
- nginx


## Step 6 — Check Running Containers

### Command:
docker ps
### Output:
backend → running  
nginx → running  


## Step 7 — Test HTTPS in Browser

Open:

https://app.local

### Output:
Backend working with HTTPS via NGINX

## Step 8 — Verify using CURL

### Command:
curl -I https://app.local

### Output:
HTTP/1.1 200 OK

### Meaning:
HTTPS is working successfully

## Step 9 — Logs Verification

### Commands:
docker logs backend
docker logs nginx

### Output:
Backend server running  
NGINX handling requests  

## NGINX Configuration

### HTTP → HTTPS Redirect

listen 80;
return 301 https://$host$request_uri;

### HTTPS Server(mkcert is not any official authority like lets encrypt)

listen 443 ssl;

ssl_certificate /etc/nginx/certs/app.local.pem;
ssl_certificate_key /etc/nginx/certs/app.local-key.pem;

### Proxy

location / {
    proxy_pass http://backend:3000;
}

## Data Flow

Browser (https://app.local)
|
NGINX (port 443)
|
SSL Termination (HTTPS → HTTP)
|
Backend (port 3000)
|
Response returned


## Key Concepts
- SSL encrypts communication
- mkcert creates local trusted certificates
- NGINX handles HTTPS (SSL termination)
- Backend runs on HTTP internally
- HTTP automatically redirects to HTTPS

## Final Result
HTTPS working  
SSL certificate configured  
HTTP -> HTTPS redirect working  
Secure communication enabled  

## Conclusion
This setup demonstrates:
- HTTPS setup using self-signed certificates  
- Reverse proxy with SSL termination  
- Secure communication using NGINX  
- Real-world production-like setup  

### <--http working for my understanding-->>
NGINX SSL handle karta hai
certificates use karta hai
browser se encrypted request aati hai
NGINX decrypt karta hai
backend ko HTTP me forward karta hai

### how certificates are made:
mkcert app.local (mkcert = ek tool hai jo LOCAL SSL certificates banata hai-->mkcert = ek tool hai jo LOCAL SSL certificates banata hai)

certificate is liek id card
# SSL Setup Documentation

## Overview
This setup demonstrates enabling HTTPS for a Docker-based application using NGINX and self-signed certificates generated with mkcert.

## Certificate Generation

SSL certificates were generated using the mkcert tool for the local domain:

app.local

Command used:

mkcert app.local

This generated two files:

- app.local.pem (certificate)
- app.local-key.pem (private key)

These files were placed inside the certs directory.

## NGINX HTTPS Configuration

NGINX was configured to handle HTTPS traffic on port 443.

The SSL configuration included:

- ssl_certificate /etc/nginx/certs/app.local.pem
- ssl_certificate_key /etc/nginx/certs/app.local-key.pem

NGINX acts as a reverse proxy and forwards requests to the backend container.

## HTTP to HTTPS Redirect

HTTP requests on port 80 are automatically redirected to HTTPS using:

return 301 https://$host$request_uri;

## Verification

The HTTPS setup was verified by opening:

https://app.local

The backend application successfully responded with:

Backend working with HTTPS via NGINX

Additionally verified using:

curl -I https://app.local
#!/bin/bash

URL="http://localhost:3000/ping" #server address
LOG="logs/health.log"  #log file path

while true
do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)  #hides output and only shows status

  if [ "$STATUS" != "200" ]; then
    echo "$(date) - FAILED - status $STATUS" >> $LOG #if server fails--> write in logs/health.log 
  fi

  sleep 10 # waits for 10 seconds
done

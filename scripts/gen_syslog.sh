#!/bin/bash

# Loop to generate log messages
while true; do
	echo "Dummy log entry at $(date)"
    	logger --rfc3164 --tag "kernel" "NOTICE: user dummy data at $(date)"
    sleep 1  # Change this to a shorter duration for more entries
done


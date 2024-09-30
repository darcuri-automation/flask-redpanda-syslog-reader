#!/bin/bash

# Loop to generate log messages
while true; do
	echo "Dummy log entry at $(date)"
    	logger "Dummy log entry at $(date)"
    sleep 1  # Change this to a shorter duration for more entries
done


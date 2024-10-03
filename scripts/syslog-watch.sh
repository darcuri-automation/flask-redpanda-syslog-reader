inotifywait -m /var/log/syslog -e modify |
while read path action file; do
    tail -n 2 /var/log/syslog | while read line; do
        echo "$line"
        echo "$line" | rpk topic produce syslog -X brokers=127.0.0.1:19092
        
        # Example command
        # ./your_command_here
    done
done


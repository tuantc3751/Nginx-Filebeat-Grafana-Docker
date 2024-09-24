# # Please do not manually call this file!
# # This script is run by the docker container when it is "run"

# # set ownership for filebeat
# chown root /etc/filebeat/filebeat.yml
# chmod 700 /etc/filebeat/filebeat.yml


# # Start filebeat in background
# filebeat &
# python3 /consumer/kafka_es.py &
# #Run the apache process in the background
# /usr/sbin/apache2ctl -D FOREGROUND &

# # Use cron service as foreground process
# cron -f


python /usr/src/app/consumer.py
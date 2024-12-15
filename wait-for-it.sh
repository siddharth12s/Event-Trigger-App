#!/bin/bash
# wait-for-it.sh

# Wait for the specified host and port to be available
# Usage: ./wait-for-it.sh host:port -- command args

TIMEOUT=60
WAIT_HOST=$1
WAIT_PORT=$2
shift 2
CMD="$@"

# Check if host and port are provided
if [[ -z "$WAIT_HOST" || -z "$WAIT_PORT" ]]; then
  echo "Usage: $0 <host>:<port> -- <command>"
  exit 1
fi

# Check if the command to run is provided
if [[ -z "$CMD" ]]; then
  echo "No command specified to run after waiting."
  exit 1
fi

# Start waiting for the service to be up
echo "Waiting for $WAIT_HOST:$WAIT_PORT to be available..."
for i in $(seq $TIMEOUT); do
  nc -z $WAIT_HOST $WAIT_PORT && break
  echo "Waiting for $WAIT_HOST:$WAIT_PORT... $i/$TIMEOUT"
  sleep 1
done

# If the service is available, run the command
if nc -z $WAIT_HOST $WAIT_PORT; then
  echo "$WAIT_HOST:$WAIT_PORT is available, executing command: $CMD"
  exec $CMD
else
  echo "$WAIT_HOST:$WAIT_PORT did not become available in time, exiting."
  exit 1
fi

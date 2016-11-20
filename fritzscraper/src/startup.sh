#!/bin/bash
set -x

pid=0

sigterm_handler() {
  if [ $pid -ne 0 ]; then
    kill -SIGTERM "$pid"
    wait "$pid"
  fi
  exit 143;
}

trap 'kill ${!}; sigterm_handler' SIGTERM

#pip install -r requirements.txt --upgrade

python fritzscraper.py &
pid="$!"

while true
do
  tail -f /dev/null & wait ${!}
done

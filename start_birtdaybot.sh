#!/bin/bash

if test -e /tmp/.birtdaybot-running; then 
    echo "script found the running file, exiting"
    kill -9 -- -$$
    exit 0 # Or any appropriate exit code
fi

cleanup() {

    echo "Cleaning up..."
    rm -f /tmp/.birtdaybot-running
    trap - EXIT SIGTERM SIGINT # clear the trap
    kill -9 -- -$$
    exit 0 # Or any appropriate exit code

}

trap "cleanup" EXIT SIGINT #####DONT HANDLE SIGTERM!!!!!!!

SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
cd "$SCRIPT_DIR"
while true; do
"$SCRIPT_DIR"/discord_bot.py; PYTHON_EXIT_CODE=$?

if [ "$PYTHON_EXIT_CODE" -ne "157" ]; then
    rm /tmp/.birtdaybot-running
else
    exit
fi
done

#!/bin/bash

cd /opt/discord-omikuji || exit 1

screen -dmS omikuji bash -c '
    source /opt/discord-omikuji/.venv/bin/activate
    cd /opt/discord-omikuji
    exec python main.py
'

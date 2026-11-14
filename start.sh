#!/bin/bash

cd /opt/discord-omikuji || exit 1

source .venv/bin/activate
python main.py

screen -S omikuji /opt/discord-omikuji/start.sh

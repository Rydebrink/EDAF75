#!/bin/bash
gnome-terminal -e python api.py

./requests.sh
python3 check-lab3.py

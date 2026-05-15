#!/bin/bash
set -euo pipefail

PROJECT_DIR="${1:-$HOME/robot_os}"

sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3 python3-tk

cd "$PROJECT_DIR"

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Robot OS environment is ready in $PROJECT_DIR"
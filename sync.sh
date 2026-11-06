#!/bin/bash
# Script 1-click để đồng bộ Git không lo conflict
# Cách dùng: ./sync.sh [Ghi chú commit]
cd "$(dirname "$0")"

MESSAGE="${1:-"Cập nhật công việc TV2"}"
python3 git_sync.py "$MESSAGE"

#!/bin/bash
/srv-st/util/backup-integration/start-backup.sh
cd /srv-st/minecraft/skelril/ && /srv-st/util/worldedit-snapshot/world-edit-backup.py
/srv-st/util/backup-integration/finish-backup.sh

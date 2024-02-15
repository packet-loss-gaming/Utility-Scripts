#!/usr/bin/env python3
#
# Copyright (c) 2015 Wyatt Childers.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import zipfile

from datetime import datetime, timedelta

date = datetime.today()
formatted_date = date.strftime('%Y-%m-%d-%H-%M-%S')

zip_filename = f"{formatted_date}.zip"

source_base_dir = "/srv-st/minecraft/skelril/"
backup_base_dir = "/srv-st/minecraft/skelril/backups"

def detect_worlds():
    worlds = {}
    for entry_name in os.listdir(source_base_dir):
        entry_path = os.path.join(source_base_dir, entry_name)
        if not os.path.isdir(entry_path):
            continue

        level_dat_path = os.path.join(entry_path, 'level.dat')
        if not os.path.exists(level_dat_path):
            continue

        worlds[entry_name] = [entry_name]
    return worlds

worlds = detect_worlds()
keep_time = timedelta(days=15)

world_subfolders = ['region', 'playerdata', 'data']

expired_file_match_regex = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}.zip$")

for world_name, world_path_parts in worlds.items():
    world_path = os.path.join(source_base_dir, *world_path_parts)
    backup_dir = os.path.join(backup_base_dir, world_name)
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print(f"Creating world backup of {world_name}...")

    with zipfile.ZipFile(os.path.join(backup_dir, zip_filename), "w", zipfile.ZIP_DEFLATED, True) as myzip:
        for subfolder_name in world_subfolders:
            subfolder = os.path.join(world_path, subfolder_name)
            for dir, subdirs, files in os.walk(subfolder):
                assets_dir = dir.replace(world_path, world_name)
                for filename in files:
                    myzip.write(os.path.join(dir, filename), os.path.join(assets_dir, filename))

        myzip.write(os.path.join(world_path, "level.dat"), os.path.join(world_name, "level.dat"))
        myzip.close()

        print(f"Backup of {world_name} created.")

    print("Checking for old backups...")
    for filename in os.listdir(backup_dir):
        if not expired_file_match_regex.match(filename):
            continue

        examined_file = os.path.join(backup_dir, filename)
        last_modified = datetime.fromtimestamp(os.path.getmtime(examined_file))
        if datetime.now() - last_modified > keep_time:
            os.remove(examined_file)
            print(f"Removing outdated backup {filename}")

print("Backup process completed.")

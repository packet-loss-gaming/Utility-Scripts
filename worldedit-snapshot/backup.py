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

def dateY(int):
    return str(int)

def dateP(int):
    return format(int, '02')

date = datetime.today()

zipFilename = dateP(date.year) + "-" + dateP(date.month) + "-" + dateP(date.day) + "-" + dateP(date.hour) + "-" + dateP(date.minute) + "-" + dateP(date.second) + ".zip"

backupBaseDir = "/srv_st/minecraft_legacy_backups"
worlds = {"City": "./City", "Halzeil": "./Halzeil", "Halzeil_nether": "./Halzeil_nether", "Astaria": "./Astaria"}
keepTime = timedelta(days=15)

worldSubfolders = ['region', 'playerdata', 'data']

for worldName, worldPath in worlds.items():
    backupDir = os.path.join(backupBaseDir, worldName)
    if not os.path.exists(backupDir):
        os.makedirs(backupDir)

    print("Creating world backup of " + worldName + "...")

    with zipfile.ZipFile(os.path.join(backupDir, zipFilename), "w", zipfile.ZIP_DEFLATED, True) as myzip:
        for subfolderName in worldSubfolders:
            subfolder = os.path.join(worldPath, subfolderName)
            for dir, subdirs, files in os.walk(subfolder):
                assetsDir = dir.replace(worldPath, worldName)
                for filename in files:
                    myzip.write(os.path.join(dir, filename), os.path.join(assetsDir, filename))

        myzip.write(os.path.join(worldPath, "level.dat"), os.path.join(worldName, "level.dat"))
        myzip.close()

        print("Backup of " + worldName + " created.")

    print("Checking for old backups...")
    fileMatchRegex = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2}.zip$")
    for filename in os.listdir(backupDir):
        if not fileMatchRegex.match(filename):
            continue

        examinedFile = os.path.join(backupDir, filename)
        lastModified = datetime.fromtimestamp(os.path.getmtime(examinedFile))
        if datetime.now() - lastModified > keepTime:
            os.remove(examinedFile)
            print("Removing outdated backup " + filename)

print("Backup process completed.")

#
# Copyright (c) 2020 Wyatt Childers.
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
import psutil

dirs = {"/ssd": "docker stop minecraft-legacy"}

for watched_dir, cmd in dirs.items():
    disc_usage = psutil.disk_usage(watched_dir)
    if disc_usage.percent > 75:
        print('Maximum disc usage for "' + watched_dir + '" exceeded')
        print('Executing "' + cmd + '"')
        os.system(cmd)
        print('Executed "' + cmd + '"')

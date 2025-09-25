'''
Copyright (C) 2024-2025 Leon Ambaum (gpl-3.0-or-later)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
from collections import Counter


log_file_path = 'common/logs/wmbusmeters.log'  # <-- set path here

ids = []

with open(log_file_path, 'r') as log_file:
    for line in log_file:
        # Search for "Received telegram from:" pattern
        match = re.search(r'Received telegram from:\s*(\d+)', line)
        if match:
            # Extract ID
            ids.append(match.group(1))

# count ids
id_counts = Counter(ids)

for id, count in id_counts.most_common():
    print(f'ID: {id} | Count: {count}')

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

------

This script generates the wmbusmeters.d config files that are read by
the wmbusmeters service from a single csv file.
'''

import csv
import os

CSV_INPUT_FILE = "wma-server/scripts/config_maker/Musterliste.csv"
CONFIGS_OUTPUT_FOLDER = "wma-server/scripts/config_maker/configured_meters"
DELIMITER=";"

# Check if output folder exists
os.makedirs(CONFIGS_OUTPUT_FOLDER, exist_ok=True)

print(f"[INFO] Ensure the csv file ({CSV_INPUT_FILE}) is having the following schema:")
print(f"[INFO] --> meter_name{DELIMITER} serial_number{DELIMITER} aes_key")
print(f"[INFO] If you have no key for the meter just leave it empty or put in 'None'")

with open(CSV_INPUT_FILE, mode="r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file, delimiter=DELIMITER)
    rows = list(reader)

    # Print total meters found
    print(f"[LOG] Found {len(rows)} meters.")

    # Create config files from each row
    for row in rows:
        # Add needed fields
        content = f"name={row['meter_name'].replace(' ', '_')}\n"
        content += f"id={row['serial_number']}\n"
        
        # Always include aes_key, set to "NOKEY" if empty
        aes_key = row.get('aes_key', '').strip()
        aes_key = aes_key if aes_key and aes_key.lower() != 'none' else 'NOKEY'
        content += f"aes_key={aes_key}\n"

        # Configure output file
        filename = f"{row['meter_name'].replace(' ', '_')}"
        output_path = os.path.join(CONFIGS_OUTPUT_FOLDER, filename)
        
        # Write config file
        print(f"[LOG] Saving \t{filename}\t to {CONFIGS_OUTPUT_FOLDER}.")
        with open(output_path, mode="w", encoding="utf-8") as output_file:
            output_file.write(content)


print("[LOG] Config files for wmbusmeters created")

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
import pandas as pd
import re

# Path to your log file
log_file = "wma-server/composing_mqtt_postgres/common/logs/wmbusmeters.log"

# Lists to store extracted data
entries = []
log_flag = 0
total_lines = sum(1 for _ in open(log_file, "r"))

# Function to print progress bar
def print_progress_bar(current, total, length=50):
    percent = current / total
    bar_length = int(length * percent)
    bar = "#" * bar_length + "-" * (length - bar_length)
    print(f"\rProcessing line number: {current} of {total_lines} [{bar}] {percent * 100:.2f}%", end="", flush=True)

# Read and parse the log file
with open(log_file, "r") as file:
    current_entry = {}
    for line_number, line in enumerate(file, start=1):
        # Logger
        if log_flag >= total_lines//100:
            #print(f"Processing line number: {line_number} of {total_lines}")
            print_progress_bar(line_number, total_lines)
            log_flag = 0
        else: 
            log_flag += 1

        line = line.strip()
        
        # Extract ID
        match_id = re.search(r"Received telegram from: (\d+)", line)
        if match_id:
            if current_entry:
                entries.append(current_entry)
            current_entry = {"ID": match_id.group(1), "Manufacturer": None}
        
        # Extract Manufacturer
        match_manufacturer = re.search(r"manufacturer: (\([^)]+\) [^(]+)", line)
        if match_manufacturer and current_entry:
            current_entry["Manufacturer"] = match_manufacturer.group(1)
    
    # Append last entry if exists
    if current_entry:
        entries.append(current_entry)

# Create DataFrame
df = pd.DataFrame(entries)

# Count occurrences per ID
result = df.groupby(["ID", "Manufacturer"]).size().reset_index(name="Count").sort_values(by=["Manufacturer", "Count"], ascending=[True, False])

# Print result
print(result)

# Save to CSV if needed
result.to_csv("wma-server/scripts/id_counts.csv", index=False)

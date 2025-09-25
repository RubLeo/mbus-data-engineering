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
import json

def generate_insert_sql(table_name, json_payload):
    # Parse the JSON string if it's not already a dictionary
    if isinstance(json_payload, str):
        json_payload = json.loads(json_payload)
    
    # Remove "_" key if present
    json_payload = {k: v for k, v in json_payload.items() if k != "_"}

    # Extract keys (column names) and values
    columns = ", ".join(f'"{key}"' for key in json_payload.keys())
    values = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in json_payload.values())

    # Construct the SQL statement
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    return sql

json_str = '{"_":"telegram","media":"heat cost allocator","meter":"fhkvdataiii","name":"MyTechem","id":"51035693","current_hca":532,"previous_hca":2179,"temp_radiator_c":25.13,"temp_room_c":22.65,"current_date":"2025-02-11T02:00:00Z","previous_date":"2024-12-31T02:00:00Z","timestamp":"2025-02-11T02:10:19Z","device":"iu891a[00202071]","rssi_dbm":-54}'

sql = generate_insert_sql("readings", json_str)

print(sql)

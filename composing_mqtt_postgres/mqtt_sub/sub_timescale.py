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
import os
from paho.mqtt import subscribe
import psycopg2

# TimescaleDB connection settings
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

timescale_uri = os.getenv("TIMESCALE_URI")
conn = psycopg2.connect(timescale_uri)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS readings (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    payload JSONB,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
''')
conn.commit()

def on_message_print(client, userdata, message):
    print(f"topic={message.topic}, payload={message.payload}")
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)

    # Insert the data into TimescaleDB (PostgreSQL table)
    cursor.execute(
        "INSERT INTO readings (topic, payload) VALUES (%s, %s)",
        (message.topic, json.dumps(data))
    )
    conn.commit()

# Subscribe to the MQTT topic
subscribe.callback(on_message_print, MQTT_TOPIC, hostname=MQTT_BROKER_HOST)

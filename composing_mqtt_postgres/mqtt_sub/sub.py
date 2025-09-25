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
import os
import psycopg2
import json
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time


# get envs
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# setup db connection
max_retries = 20
retry_delay = 3
conn = None
for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()
        print(f"Connection attempt {attempt + 1}/{max_retries} succeded")
        break  # connected
    except psycopg2.OperationalError as e:
        print(f"Connection attempt {attempt + 1}/{max_retries} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            raise  # give up


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


def on_message_print(client, userdata, message):
    print(f"topic={message.topic}, payload={message.payload}")
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    sql = generate_insert_sql("readings", data)
    print(f"inserting to db with {sql}")
    cursor.execute(sql)
    conn.commit()

subscribe.callback(on_message_print, MQTT_TOPIC, hostname=MQTT_BROKER_HOST)





# # MQTT callback
# def on_message(client, userdata, message):
#     payload = message.payload.decode('utf-8')
#     data = json.loads(payload)
#     cursor.execute("INSERT INTO readings (key) VALUES (%s)", (data['key']))
#     conn.commit()

# while True:
#     msg = subscribe.simple(MQTT_TOPIC, hostname=MQTT_BROKER_HOST)
#     print(msg)

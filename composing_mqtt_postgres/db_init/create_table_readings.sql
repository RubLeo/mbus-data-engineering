/*
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
*/
CREATE TABLE readings (
    uuid SERIAL PRIMARY KEY,
    id INT,
    media TEXT,
    meter TEXT,
    name TEXT,
    current_hca INT,
    previous_hca INT,
    temp_radiator_c FLOAT,
    temp_room_c FLOAT,
    "current_date" TIMESTAMP WITH TIME ZONE,
    previous_date TIMESTAMP WITH TIME ZONE,
    timestamp TIMESTAMP WITH TIME ZONE,
    device TEXT,
    rssi_dbm INT
);

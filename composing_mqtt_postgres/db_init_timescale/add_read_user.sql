/*Copyright (C) 2024-2025 Leon Ambaum (gpl-3.0-or-later)

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
-- Create a new read-only user
CREATE USER wmreader WITH PASSWORD 'secret';

-- Grant CONNECT permission on the database
GRANT CONNECT ON DATABASE database TO wmreader;

-- Grant USAGE on the schema (e.g., public schema)
GRANT USAGE ON SCHEMA public TO wmreader;

-- Grant SELECT permissions on all tables in the schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO wmreader;

-- Grant SELECT on all future tables as well
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO wmreader;

-- Prevent modifications by explicitly REVOKING all write permissions
REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA public FROM wmreader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE INSERT, UPDATE, DELETE, TRUNCATE ON TABLES FROM wmreader;

-- Ensure the user cannot modify sequences (auto-increment fields)
REVOKE USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public FROM wmreader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE USAGE, SELECT, UPDATE ON SEQUENCES FROM wmreader;

-- Prevent function execution if necessary (optional)
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM wmreader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE EXECUTE ON FUNCTIONS FROM wmreader;

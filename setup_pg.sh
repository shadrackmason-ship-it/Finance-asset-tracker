#!/bin/bash
psql -c "CREATE USER masontrack WITH PASSWORD 'Mt@Secure2025!';"
psql -c "CREATE DATABASE masontrack_db OWNER masontrack;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE masontrack_db TO masontrack;"
psql -c "ALTER USER masontrack CREATEDB;"
echo "Done! Database and user created."

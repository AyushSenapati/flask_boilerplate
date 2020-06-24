#!/bin/sh

set -e
set -u

function create_database() {
    local database=$1
    echo "Creating database '$database'"
    psql --user "$DB_OWNER" <<-EOSQL
        CREATE DATABASE $database;
EOSQL
}

if [ -n "$DATABASES" ]; then
    echo "Databases to be created: $DATABASES"
    for db in $(echo $DATABASES | tr ',' ' '); do
        create_database $db
    done
    echo "Databases created"
fi
#!/bin/bash

MDB_PATH=$1
CSV_PATH=$2

for i in `mdb-tables "$MDB_PATH"`; do
    echo "$i"
done

echo
echo "Choose table to export.?"
read table

mdb-export "$MDB_PATH" "$table" > "$CSV_PATH"

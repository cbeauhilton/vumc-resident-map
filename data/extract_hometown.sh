#!/bin/sh
rm -f hometown.db
sqlite3 hometown.db '.read extract_hometown.sql'

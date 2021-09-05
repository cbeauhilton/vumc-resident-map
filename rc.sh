#!/bin/sh

here=$PWD

uvlog="logs/app.log"
scrapelog="logs/scrape.log"
maplog="logs/map.log"
dbfile="data/database.db"

# clean up old runs
echo "" > $uvlog
echo "" > $scrapelog
echo "" > $maplog

nohup uvicorn app:app --port 9000 > $uvlog &
sleep 5

nohup python -u scrape.py > $scrapelog

nohup python -u map.py > $maplog &

uvpid=$(ps aux | grep 'uvicorn app:app' | grep -v grep | awk {'print $2'} | xargs)
mappid=$(ps aux | grep 'map.py' | grep -v grep | awk {'print $2'} | xargs)

# If this script is killed, kill the processes.
trap "kill $mappid 2> /dev/null" EXIT

# While the python script is running,
# regenerate the database with new data.
while kill -0 $mappid 2> /dev/null; do
    sleep 3
    cd $here
    cd data/
    sqlite3 hometown.db '.read extract_hometown.sql'
done

# one final refresh
cd $here
cd data/
sqlite3 hometown.db '.read extract_hometown.sql'

# Disable the trap on a normal exit.
trap - EXIT

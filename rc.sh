#!/bin/sh

here=$PWD

uvlog="logs/app.log"
scrapelog="logs/scrape.log"
maplog="logs/map.log"
dslog="logs/ds.log"
dbfile="data/database.db"
dsfile="data/hometown.db"

# clean up old runs
echo "" > $uvlog
echo "" > $scrapelog
echo "" > $maplog
echo "" > $dslog
rm -f $dsfile

nohup uvicorn app:app --port 9000 > $uvlog &
uvpid=$(ps aux | grep 'uvicorn app:app' | grep -v grep | awk {'print $2'} | xargs)
sleep 5

nohup python -u scrape.py > $scrapelog &&

nohup python -u map.py > $maplog &
mappid=$(ps aux | grep 'map.py' | grep -v grep | awk {'print $2'} | xargs)
sleep 30

cd data/
rm -f hometown.db
sqlite3 hometown.db '.read extract_hometown.sql'
nohup datasette hometown.db --setting default_page_size 200 > ../$dslog &
dspid=$(ps aux | grep 'datasette' | grep -v grep | awk {'print $2'} | xargs)
cd $here

# make new database if big enough, start ds server
# if [ -n "$(find "$dbfile" -prune -size +10000c)" ]; then
#   cd data/
#   sqlite3 hometown.db '.read extract_hometown.sql'
#   nohup datasette hometown.db --setting default_page_size 200 > ../$dslog &
#   dspid=$(ps aux | grep 'datasette' | grep -v grep | awk {'print $2'} | xargs)
#   cd $here
# fi

# If this script is killed, kill the processes.
# trap "kill $mappid 2> /dev/null" EXIT
trap "kill $uvpid 2> /dev/null" EXIT

# While the python script is running,
# regenerate the database with new data.
while kill -0 $mappid 2> /dev/null; do
    sleep 15 
    cd data/
    rm -f hometown.db
    sqlite3 hometown.db '.read extract_hometown.sql'
    sleep 30
    cd $here
done

# one final refresh
cd data/
rm -f hometown.db
sqlite3 hometown.db '.read extract_hometown.sql'
cd $here

# kill $uvpid
# kill $dspid

# Disable the trap on a normal exit.
trap - EXIT

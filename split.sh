#!/bin/sh

# Split the files when the string CREATE TABLE is found
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
##### OPTIONS VERIFICATION #####

if [ -z "$1" ]; then
  echo "Need parametr. Example ( ./Split_db.sh ./master.sql )"
 exit 1
fi

csplit -n 4 -k $1 '/^DROP TABLE IF EXISTS .*/' '{800}'


# Read the first line, extract table name and rename the file
for f in $(ls xx*);
do
table_name=`head -1 $f | awk '{ sub(/.*DROP TABLE IF EXISTS /, ""); sub(/ .*/, ""); print }'`
if [[ "$f" != *"xx0000"* ]];then
  printf '%s\n' "$f"
  cat "xx0000" $f > "$table_name.sql"
  rm $f
fi
done;
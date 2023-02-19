# Calculate stats for data files.
#!/usr/bin/env bash

for datafile in "$@" # $@ in refers to all of a shell script's command-line arguments. $1 , $2 , etc.,
                     # Place variables in quotes if the values might have spaces in them
do
    echo $datafile
    bash goostats $datafile stats-$datafile
done

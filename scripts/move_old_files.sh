#!/bin/bash

# Ensure a directory is passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <from_directory>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Usage: $0 <to_directory>"
    exit 1
fi

# Assign the first argument to DIR
FROM_DIR=$1
TO_DIR=$2

# Check if directories exists
if [ ! -d "$FROM_DIR" ]; then
    echo "Error: From Directory $FROM_DIR does not exist."
    exit 1
fi

if [ ! -d "$TO_DIR" ]; then
    echo "Error: To Directory $TO_DIR does not exist."
    exit 1
fi

# [!] hard coded value
# Find and delete files older than 90 days in the specified directory
find "$FROM_DIR" -type f -mtime +90 -exec mv -v {} $TO_DIR \;

# Optionally, print a message indicating completion
echo "Stashed files older than 90 days ($FROM_DIR --> $TO_DIR)"

echo "File count in target directory (long term storage):" `ls $TO_DIR | wc -l`
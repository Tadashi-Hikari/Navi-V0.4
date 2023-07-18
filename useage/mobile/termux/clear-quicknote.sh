#!/bin/bash
# This script was desinged to be used with the application Markor, so I could have a note app that will not interfere w/ my ADHD

source_path=~/Lab/notebook/quicknote.md
target_directory=~/Lab/notebook/archived-quicknotes/

# Get the current date
formatted_date=$(date "+%Y-%m-%d")
target_filename="${formatted_date}-quicknote.md"
target_path="${target_directory}/${target_filename}"

# Copy the contents of the source file to the target file
cp $source_path $target_path

# Delete the source file
rm $source_path

# Create a new empty source file
touch $source_path
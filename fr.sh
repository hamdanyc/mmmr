#!/bin/bash

# Target folder where the CSV files are located
FOLDER="tempahan"

# Check if the folder exists
if [ ! -d "$FOLDER" ]; then
    echo "Error: Directory '$FOLDER' not found. Please create it and place your files inside."
    exit 1
fi

# Initialize the counter for the new file names
count=1

# Change to the directory to make the commands simpler
cd "$FOLDER" || exit

# List all files that start with 'grp' and end with '.csv'
# Sort them to ensure they are renamed in a predictable order (by original name)
for original_file in $(ls grp*.csv | sort -V); do
    # 1. Extract the descriptive part of the filename after the first '-'
    #    The regex pattern "grp*-" removes the leading 'grp' and its number/letter suffix.
    #    This isolates the part like "diraja.csv", "weststar.csv", etc.
    descriptive_part=$(echo "$original_file" | sed -E 's/grp.*-//')

    # 2. Construct the new filename
    #    New name will be "grp" + current count + "-" + descriptive part
    new_file="grp${count}-${descriptive_part}"

    # 3. Perform the rename operation
    echo "Renaming: $original_file -> $new_file"
    mv "$original_file" "$new_file"

    # 4. Increment the counter
    count=$((count + 1))
done

echo "Batch renaming complete. $count files were renamed starting from grp1."

# Return to the original directory
cd - > /dev/null
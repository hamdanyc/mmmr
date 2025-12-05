#!/bin/bash

# A script to rename files that start with 'grpN' where N is a number,
# by incrementing N by 1 sequentially based on the file's order in file-re.txt.
# This version reads the list of filenames from 'file-re.txt'.

# ----------------------------------------------------------------
# --- Configuration ---
# ----------------------------------------------------------------

# Set to true to see what the script *would* do (dry run).
# Set to false to actually perform the file renaming/creation and moving.
DRY_RUN=false

# The directory containing the source files (e.g., the original files named in file-re.txt).
INPUT_SOURCE_DIR="./tempahan"

# The input file containing the list of filenames to process.
INPUT_FILE="file-re.txt"

# The directory where the renamed/created files will be stored.
# This directory will be created if it does not exist when DRY_RUN is false.
OUTPUT_DIR="./temp_data"

# ----------------------------------------------------------------
# --- Function to handle renaming logic ---
# This function now accepts the desired new number as a second argument.
# ----------------------------------------------------------------
rename_file() {
    local old_name="$1"
    local new_number="$2"
    
    # Check if the old_name is empty, skip if so.
    if [ -z "$old_name" ]; then
        return
    fi
    
    # Use 'case' for portable pattern matching and extraction (replaces BASH-specific regex)
    case "$old_name" in
        # Pattern to match: grp followed by one or more digits, then a hyphen, then anything else
        grp[0-9]*-*)
            # 1. Extraction using POSIX parameter expansion:
            
            # Extract the part before the first hyphen (e.g., 'grp16')
            local grp_and_num="${old_name%%-*}"
            
            # Extract the part after the first hyphen (e.g., 'Istana-Perlis.csv')
            local suffix_part="${old_name#$grp_and_num-}"
            
            # The new number (new_number) is provided by the main loop counter.
            
            # 2. Construct the new filename and define full source/target paths
            local new_name="grp${new_number}-${suffix_part}"
            
            # Full path to the original file in the source directory
            local source_path="${INPUT_SOURCE_DIR}/${old_name}"
            
            # Full path to the new file in the output directory
            local target_path="${OUTPUT_DIR}/${new_name}"
            
            # 3. Execute or display the rename, move, or creation operation
            if $DRY_RUN; then
                # Show the original group number just for clarity in the dry run output
                local original_grp_num="${grp_and_num#grp}"
                echo "DRY RUN (Original: grp${original_grp_num}): '$source_path' -> '$target_path'"
            else
                # Check if the source file physically exists in the INPUT_SOURCE_DIR
                if [ -e "$source_path" ]; then
                    echo "File EXISTS: Renaming and moving '$source_path' -> '$target_path'"
                    # The mv command performs both rename and move in one step
                    mv -- "$source_path" "$target_path"
                else
                    echo "File MISSING: Creating new empty file at '$target_path'"
                    # Create a new empty file with the desired name in the output directory
                    touch "$target_path"
                fi
            fi
            ;;
        *)
            # This handles lines in file-re.txt that do not start with the expected pattern.
            echo "Skipping '$old_name': Does not match the expected 'grpN-SUFFIX' format."
            ;;
    esac
}

# ----------------------------------------------------------------
# --- Main Execution ---
# ----------------------------------------------------------------

echo "--- File Renaming/Creation Script (Reading from $INPUT_FILE) ---"

# Initialize the sequential counter. The target sequence is 1, 2, 3, 4...
count=0
new_grp_num=0 

# Check if the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input file '$INPUT_FILE' not found." >&2
    echo "Please ensure '$INPUT_FILE' is in the current directory." >&2
    exit 1
fi

if $DRY_RUN; then
    echo "!!! Currently running in DRY-RUN mode. No files will be renamed or moved. !!!"
    echo "Source directory: $INPUT_SOURCE_DIR"
    echo "Target output directory: $OUTPUT_DIR"
    echo "New Group Number Sequence: 1, 2, 3, 4, ..."
    echo "If a source file is missing, the dry run assumes renaming would happen."
    echo "To perform the rename/create, change DRY_RUN=true to DRY_RUN=false at the top of the script."
else
    # If not a dry run, ensure the source and output directories exist
    
    # 1. Check/create OUTPUT_DIR
    if [ ! -d "$OUTPUT_DIR" ]; then
        echo "Creating output directory: '$OUTPUT_DIR'"
        mkdir -p "$OUTPUT_DIR"
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to create output directory '$OUTPUT_DIR'. Exiting." >&2
            exit 1
        fi
    fi
    
    # 2. Delete existing files from OUTPUT_DIR
    if [ -d "$OUTPUT_DIR" ]; then
        echo "Clearing existing files from output directory: '$OUTPUT_DIR'"
        # Safely delete all files and subdirectories within OUTPUT_DIR but keep OUTPUT_DIR itself
        find "$OUTPUT_DIR" -mindepth 1 -delete
        if [ $? -ne 0 ]; then
             echo "WARNING: Could not clear all files from '$OUTPUT_DIR'." >&2
        fi
    fi
    
    # 3. Check INPUT_SOURCE_DIR (we don't create it, as the source files should already be there)
    if [ ! -d "$INPUT_SOURCE_DIR" ]; then
        echo "ERROR: Source directory '$INPUT_SOURCE_DIR' not found." >&2
        echo "Please ensure your files are inside '$INPUT_SOURCE_DIR'." >&2
        exit 1
    fi

    echo "!!! Performing ACTUAL RENAMES (if file exists) or CREATING (if file missing) and MOVING from '$INPUT_SOURCE_DIR' to '$OUTPUT_DIR'. !!!"
fi
echo "--------------------------------------------------------"

# Read the file names from the input file line by line, preserving order.
while IFS= read -r file_name; do
    
    # 1. Update the sequential group number (1, 2, 3, 4...)
    # Since 'count' starts at 0, adding 1 provides the desired sequential number (1, 2, 3...).
    new_grp_num=$((count + 1))

    count=$((count + 1)) # Increment file counter

    # 2. Process the file name
    # Remove leading/trailing whitespace just in case
    file_name=$(echo "$file_name" | xargs)
    
    # Pass the calculated new number to the renaming function
    rename_file "$file_name" "$new_grp_num"

done < "$INPUT_FILE"

echo "--------------------------------------------------------"
echo "Script finished."
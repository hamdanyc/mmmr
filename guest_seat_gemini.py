import pandas as pd
import os
import re

# --- CONFIGURATION ---
# Define table sizes and starting numbers
TABLE_START_NUMBER = 13
STANDARD_TABLE_CAPACITY = 8
DIRAJA_TABLE_CAPACITY = 9

def read_csv_file(filename):
    """Read a CSV file and return a DataFrame."""
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return pd.DataFrame()

def write_csv_file(df, filename):
    """Write a DataFrame to a CSV file."""
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

def assign_seats(guests_df):
    """Assign table and seat numbers to guests, ensuring groups sit together."""
    main_guests = []
    table_counter = TABLE_START_NUMBER
    
    # Process each group separately in the order they were read
    for gp_id, group_df in guests_df.groupby('gp_id'):
        # Ensure the dataframe is properly indexed for slicing
        group_df = group_df.sort_values(by='original_order').reset_index(drop=True)
        
        gp_name = group_df['gp_name'].iloc[0]
        
        # Determine capacity based on group type
        if gp_name.lower() == "diraja":
            guests_per_table = DIRAJA_TABLE_CAPACITY
        else:
            guests_per_table = STANDARD_TABLE_CAPACITY
            
        num_guests = len(group_df)
        num_tables = (num_guests + guests_per_table - 1) // guests_per_table
        
        total_seats_needed = num_tables * guests_per_table
        remaining_seats = total_seats_needed - num_guests
        
        # Add 'Simpanan' (Reserve) entries for remaining seats
        if remaining_seats > 0:
            reserve_data = [{'name': 'Simpanan', 'menu': 'N/A', 'gp_id': gp_id, 'gp_name': gp_name}] * remaining_seats
            group_df = pd.concat([group_df, pd.DataFrame(reserve_data)], 
                                   ignore_index=True)
        
        # Assign tables for this group
        for table_num_in_group in range(num_tables):
            start_index = table_num_in_group * guests_per_table
            end_index = (table_num_in_group + 1) * guests_per_table
            
            table_df = group_df.iloc[start_index:end_index].copy()
            
            # Assign table number
            current_table_number = table_counter
            table_df['table_number'] = current_table_number
            
            # Assign seat number (The critical correction: seat must be relative to the table's start index)
            # The indices are 0 to (guests_per_table - 1). Adding 1 makes them 1 to guests_per_table.
            table_df['seat'] = table_df.index - start_index + 1
            
            main_guests.append(table_df)
            table_counter += 1
    
    # Combine all main guests
    main_guests_df = pd.concat(main_guests, ignore_index=True)
    
    # Sort by table and seat for final output
    main_guests_df = main_guests_df.sort_values(by=['table_number', 'seat'])
    
    # Final cleanup of columns
    final_columns = ['table_number', 'seat', 'name', 'menu', 'gp_id', 'gp_name']
    return main_guests_df[final_columns]

def process_guest_files():
    """Process all guest files and assign seating."""
    tempahan_folder = 'tempahan'
    
    if not os.path.exists(tempahan_folder):
        print(f"Error: Folder '{tempahan_folder}' not found. Please create it and place CSV files inside.")
        return pd.DataFrame()
        
    group_files = [f for f in os.listdir(tempahan_folder) if f.startswith('grp') and f.endswith('.csv')]
    
    # Sort files numerically based on the number in the filename (e.g., grp1 before grp10)
    group_files.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    
    guests = []
    global_guest_counter = 0 # To preserve the original reading order
    
    for file in group_files:
        file_path = os.path.join(tempahan_folder, file)
        group_df = read_csv_file(file_path)
        
        if group_df.empty:
            continue
            
        # Extract numeric gp_id from filename (the number after 'grp')
        gp_id_match = re.search(r'grp(\d+)', file)
        gp_id = int(gp_id_match.group(1)) if gp_id_match else 0
        
        # Extract group name from filename (text after the first '-' up to the extension)
        gp_name_match = re.search(r'-(.*?)\.csv$', file)
        gp_name = gp_name_match.group(1).strip() if gp_name_match else "unknown"
        
        group_df['gp_id'] = gp_id
        group_df['gp_name'] = gp_name
        
        # Set default menu to 'Daging' if menu is NULL or not present
        if 'menu' not in group_df.columns:
            group_df['menu'] = 'Daging'
        else:
            group_df['menu'] = group_df['menu'].fillna('Daging')
        
        # Only include guests with valid names
        valid_guests = group_df[~group_df['name'].isnull() & (group_df['name'] != '')].copy()
        
        # Add a column to preserve the initial read order of guests
        valid_guests['original_order'] = range(global_guest_counter, global_guest_counter + len(valid_guests))
        global_guest_counter += len(valid_guests)
        
        guests.append(valid_guests)
    
    # Combine all guests
    if not guests:
        print("No valid guest data found.")
        return pd.DataFrame()
        
    guests_df = pd.concat(guests, ignore_index=True)
    
    # Assign seats
    final_guests_df = assign_seats(guests_df)
    
    # Save to guest_seat.csv
    write_csv_file(final_guests_df, 'guest_seat.csv')
    
    return final_guests_df

if __name__ == '__main__':
    final_guests = process_guest_files()
    if not final_guests.empty:
        print("✅ Guest seating assignment completed. See guest_seat.csv for details.")
    else:
        print("❌ Guest seating assignment failed or no data processed.")
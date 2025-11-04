import pandas as pd
import os
import re

def read_csv_file(filename):
    """Read a CSV file and return a DataFrame."""
    return pd.read_csv(filename)

def write_csv_file(df, filename):
    """Write a DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

def assign_seats(guests_df):
    """Assign table and seat numbers to guests, ensuring groups sit together."""
    main_guests = []
    table_counter = 13  # Start tables from 13
    
    # Process each group separately in the order they were read
    for gp_id, group_df in guests_df.groupby('gp_id'):
        group_df = group_df.reset_index(drop=True)
        
        # Calculate how many tables we need for this group
        if table_counter in [1, 2]:
            guests_per_table = 9
        else:
            guests_per_table = 8
            
        num_tables = len(group_df) // guests_per_table
        remaining_guests = len(group_df) % guests_per_table
        
        # If there are remaining guests, add one more table
        if remaining_guests > 0:
            num_tables += 1
            
            # If we have simpanan, use them to fill remaining seats
            # We no longer use simpanan, so just add reserve entries
            for _ in range(guests_per_table - remaining_guests):
                group_df = pd.concat([group_df, pd.DataFrame([{'name': 'reserve', 'menu': '', 'gp_id': gp_id}])], 
                                   ignore_index=True)
        
        # Assign tables for this group
        for table_num in range(num_tables):
            table_df = group_df.iloc[table_num*guests_per_table:(table_num+1)*guests_per_table].copy()
            table_df['table_number'] = table_counter
            if table_counter in [1, 2]:
                # For tables 1 and 2 with 9 guests, seat numbers go from 1-9
                table_df['seat'] = (table_df.index % 9) + 1
            else:
                # For other tables with 8 guests, seat numbers go from 1-8
                table_df['seat'] = (table_df.index % 8) + 1
            main_guests.append(table_df)
            table_counter += 1
    
    # Combine all main guests
    main_guests_df = pd.concat(main_guests)
    
    # Sort by table and seat for final output
    main_guests_df = main_guests_df.sort_values(by=['table_number', 'seat'])
    
    return main_guests_df

def process_guest_files():
    """Process all guest files and assign seating."""
    # Read group files from tempahan folder (grp1.csv, grp2.csv, etc.)
    tempahan_folder = 'tempahan'
    group_files = [f for f in os.listdir(tempahan_folder) if f.startswith('grp') and f.endswith('.csv')]
    
    # Sort files numerically based on the number in the filename
    group_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    
    guests = []
    
    for file in group_files:
        file_path = os.path.join(tempahan_folder, file)
        group_df = read_csv_file(file_path)
        
        # Extract numeric gp_id from filename (the number after 'grp')
        gp_id_match = re.search(r'grp(\d+)', file)
        if gp_id_match:
            gp_id = int(gp_id_match.group(1))
        else:
            gp_id = 0  # Default value if no number is found
        
        # Extract group name from filename (text after '-')
        gp_name_match = re.search(r'-(.*?)(?:\.|$)', file)
        if gp_name_match:
            gp_name = gp_name_match.group(1)
        else:
            gp_name = "unknown"
        
        group_df['gp_id'] = gp_id  # Add gp_id with numeric group identifier
        group_df['gp_name'] = gp_name  # Add gp_name with group name from filename
        
        # Set default menu to 'Daging' if menu is NULL or not present
        if 'menu' not in group_df.columns:
            group_df['menu'] = 'Daging'
        else:
            group_df['menu'] = group_df['menu'].fillna('Daging')
        
        # Only include guests with valid names
        valid_guests = group_df[~group_df['name'].isnull() & (group_df['name'] != '')]
        guests.append(valid_guests)
    
    # Combine all guests
    guests_df = pd.concat(guests)
    
    # Assign seats
    guests_df = assign_seats(guests_df)
    
    # Save to guest_seat.csv
    write_csv_file(guests_df, 'guest_seat.csv')
    
    return guests_df

if __name__ == '__main__':
    final_guests = process_guest_files()
    print("Guest seating assignment completed. See guest_seat.csv for details.")

import pandas as pd
import os
import re

def read_csv_file(filename):
    """Read a CSV file and return a DataFrame."""
    return pd.read_csv(filename)

def write_csv_file(df, filename):
    """Write a DataFrame to a CSV file."""
    df.to_csv(filename, index=False)

def assign_seats(guests_df, simpanan_df):
    """Assign table and seat numbers to guests, ensuring groups sit together."""
    main_guests = []
    table_counter = 13  # Start tables from 13
    
    # Process each group separately in the order they were read
    for gp_id, group_df in guests_df.groupby('gp_id'):
        group_df = group_df.reset_index(drop=True)
        
        # Calculate how many tables we need for this group
        num_tables = len(group_df) // 8
        remaining_guests = len(group_df) % 8
        
        # If there are remaining guests, add one more table
        if remaining_guests > 0:
            num_tables += 1
            
            # If we have simpanan, use them to fill remaining seats
            if not simpanan_df.empty:
                needed_simpanan = 8 - remaining_guests
                simpanan_to_add = simpanan_df.head(needed_simpanan)
                group_df = pd.concat([group_df, simpanan_to_add], ignore_index=True)
                # Update simpanan_df directly
                simpanan_df = simpanan_df.drop(simpanan_to_add.index).reset_index(drop=True)
            else:
                # If no simpanan, add "reserve" entries for remaining seats
                for _ in range(8 - remaining_guests):
                    group_df = pd.concat([group_df, pd.DataFrame([{'name': 'reserve', 'menu': '', 'gp_id': gp_id}])], 
                                       ignore_index=True)
        
        # Assign tables for this group
        for table_num in range(num_tables):
            table_df = group_df.iloc[table_num*8:(table_num+1)*8].copy()
            table_df['table_number'] = table_counter
            table_df['seat'] = (table_df.index % 8) + 1
            main_guests.append(table_df)
            table_counter += 1
    
    # Combine all main guests
    main_guests_df = pd.concat(main_guests)
    
    # Sort by table and seat for final output
    main_guests_df = main_guests_df.sort_values(by=['table_number', 'seat'])
    
    return main_guests_df, simpanan_df

def process_guest_files():
    """Process all guest files and assign seating."""
    # Read group files from tempahan folder (grp1.csv, grp2.csv, etc.)
    tempahan_folder = 'tempahan'
    group_files = [f for f in os.listdir(tempahan_folder) if f.startswith('grp') and f.endswith('.csv')]
    
    # Sort files numerically based on the number in the filename
    group_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    
    guests = []
    simpanan = []
    
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
        
        # Identify guests with missing names (for simpanan)
        missing_names = group_df[group_df['name'].isnull() | (group_df['name'] == '')]
        valid_guests = group_df[~group_df['name'].isnull() & (group_df['name'] != '')]
        
        if not missing_names.empty:
            simpanan.append(missing_names)
        
        guests.append(valid_guests)
    
    # Combine all guests and simpanan
    guests_df = pd.concat(guests)
    simpanan_df = pd.concat(simpanan) if simpanan else pd.DataFrame()
    
    # Assign seats
    guests_df, simpanan_df = assign_seats(guests_df, simpanan_df)
    
    # Save to guest_seat.csv
    write_csv_file(guests_df, 'guest_seat.csv')
    
    # Save simpanan to a separate file
    if not simpanan_df.empty:
        write_csv_file(simpanan_df, 'simpanan_guests.csv')
    
    return guests_df

if __name__ == '__main__':
    final_guests = process_guest_files()
    print("Guest seating assignment completed. See guest_seat.csv for details.")
    if os.path.exists('simpanan_guests.csv'):
        print("Simpanan guests saved to simpanan_guests.csv")

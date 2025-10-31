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
    # Sort by group to ensure guests from the same group sit together
    guests_df = guests_df.sort_values(by='gp_id')
    
    # Reset index for proper seating assignment
    guests_df = guests_df.reset_index(drop=True)
    
    # Calculate table numbers (each table has 8 guests), starting from 13
    guests_df['table_number'] = (guests_df.index // 8) + 13
    
    # Calculate seat numbers (1-8 per table)
    guests_df['seat'] = (guests_df.index % 8) + 1
    
    return guests_df

def process_guest_files():
    """Process all guest files and assign seating."""
    # Read group files from tempahan folder (grp1.csv, grp2.csv, etc.)
    tempahan_folder = 'tempahan'
    group_files = [f for f in os.listdir(tempahan_folder) if f.startswith('grp') and f.endswith('.csv')]
    group_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))
    
    guests = []
    
    for file in group_files:
        file_path = os.path.join(tempahan_folder, file)
        group_df = read_csv_file(file_path)
        
        # Extract gp_id from filename (text after the last '-')
        category_match = re.search(r'-(.*?)(?=\.)', file)
        if category_match:
            gp_id = category_match.group(1).lower()
        else:
            gp_id = "unknown"
        
        group_df['gp_id'] = gp_id  # Add gp_id with group identifier
        
        # Set default menu to 'Daging' if menu is NULL or not present
        if 'menu' not in group_df.columns:
            group_df['menu'] = 'Daging'
        else:
            group_df['menu'] = group_df['menu'].fillna('Daging')
        
        guests.append(group_df)
    
    # Combine all guests
    guests_df = pd.concat(guests, ignore_index=True)
    
    # Assign seats
    guests_df = assign_seats(guests_df)
    
    # Add reserve seats (vacant seats marked as 'reserve')
    total_guests = len(guests_df)
    # Calculate starting table number (13) and total tables needed
    first_table = 13
    last_table = ((total_guests - 1) // 8) + first_table
    # total_tables = last_table - first_table + 1
    
    # Create DataFrame for reserve seats. Table start #13
    reserve_seats = []
    for table in range(first_table, last_table + 1):
        table_seats = guests_df[guests_df['table_number'] == table]['seat'].tolist()
        for seat in range(1, 9):
            if seat not in table_seats:
                reserve_seats.append({
                    'name': 'simpanan',
                    'menu': 'simpanan',
                    'table_number': table,
                    'seat': seat,
                    'gp_id': 'simpanan'
                })
    
    # Add reserve seats to the main DataFrame
    reserve_df = pd.DataFrame(reserve_seats)
    guests_df = pd.concat([guests_df, reserve_df], ignore_index=True)
    
    # Sort by table and seat for final output
    guests_df = guests_df.sort_values(by=['table_number', 'seat'])
    
    # Save to guest_final.csv
    write_csv_file(guests_df, 'guest_seat.csv')
    
    return guests_df

if __name__ == '__main__':
    final_guests = process_guest_files()
    print("Guest seating assignment completed. See guest_seat.csv for details.")

import pandas as pd
import os
import re

# --- CONFIGURATION ---
STANDARD_TABLE_CAPACITY = 8
DIRAJA_TABLE_CAPACITY = 9
RESERVE_FILE_NAME = 'data/reserve.csv' 
DEFAULT_MENU = 'Daging'

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

# --- DATA CLEANING ROUTINE (FIXED) ---
def clean_guest_data(df):
    """
    Performs essential data cleaning and standardization on the raw guest DataFrame.
    
    Ensures names and menus are standardized and invalid records are removed.
    """
    if df.empty:
        return df

    # 1. Strip whitespace from all string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # 2. Case Standardization for 'name'
    if 'name' in df.columns:
        df['name'] = df['name'].str.title()

    # 3. Handle Missing/Empty 'menu' data
    if 'menu' not in df.columns:
        df['menu'] = DEFAULT_MENU
    else:
        # FIX: Remove inplace=True and assign back to avoid FutureWarning
        df['menu'] = df['menu'].replace('', DEFAULT_MENU)
        # Fill NaN values with the default menu
        df['menu'] = df['menu'].fillna(DEFAULT_MENU)

    # 4. Filter out records where 'name' is empty or invalid
    df = df[~df['name'].isnull() & (df['name'] != '') & (df['name'] != 'Nan')].copy()

    return df
# --- END DATA CLEANING ROUTINE ---

def assign_seats(guests_df):
    """Assign table and seat numbers to guests, ensuring groups sit together."""
    
    if guests_df.empty:
        return pd.DataFrame()
        
    main_guests = []
    
    min_gp_id = guests_df['gp_id'].min()
    table_counter = min_gp_id
    
    for gp_id, group_df in guests_df.groupby('gp_id'):
        
        # Ensure table assignment starts at least from the gp_id
        table_counter = max(table_counter, gp_id)
        
        group_df = group_df.sort_values(by='original_order').reset_index(drop=True)
        gp_name = group_df['gp_name'].iloc[0]
        
        if gp_name.lower() == "diraja" or gp_name.lower()=="ramli":
            guests_per_table = DIRAJA_TABLE_CAPACITY
        else:
            guests_per_table = STANDARD_TABLE_CAPACITY
            
        num_guests = len(group_df)
        num_tables = (num_guests + guests_per_table - 1) // guests_per_table
        
        total_seats_needed = num_tables * guests_per_table
        remaining_seats = total_seats_needed - num_guests
        
        if remaining_seats > 0:
            reserve_data = [{'name': 'Simpanan', 'menu': 'N/A', 'gp_id': 0, 'gp_name': 'RESERVE_SEAT', 'original_order': -1}] * remaining_seats
            group_df = pd.concat([group_df, pd.DataFrame(reserve_data)], 
                                   ignore_index=True)
        
        for table_num_in_group in range(num_tables):
            start_index = table_num_in_group * guests_per_table
            
            table_df = group_df.iloc[start_index:start_index + guests_per_table].copy()
            
            current_table_number = table_counter
            table_df['table_number'] = current_table_number
            
            table_df['seat'] = table_df.index - start_index + 1
            
            main_guests.append(table_df)
            table_counter += 1
    
    main_guests_df = pd.concat(main_guests, ignore_index=True)
    
    main_guests_df = main_guests_df.sort_values(by=['table_number', 'seat']).reset_index(drop=True)
    
    final_columns = ['table_number', 'seat', 'name', 'menu', 'gp_id', 'gp_name']
    return main_guests_df[final_columns]

def process_reserve_guests():
    """Read reserve.csv and prepare reserve guests list."""
    reserve_df = read_csv_file(RESERVE_FILE_NAME)
    
    # Clean the raw reserve data immediately after reading
    reserve_df = clean_guest_data(reserve_df)
    
    if reserve_df.empty:
        return []
        
    valid_reserve_guests = reserve_df.to_dict('records')
    
    return valid_reserve_guests

def fill_vacant_seats(assigned_df, reserve_guests_list):
    """Replace 'Simpanan' entries in the assigned DataFrame with reserve guests."""
    
    if not reserve_guests_list:
        print("No reserve guests available to fill vacant seats.")
        return assigned_df
        
    simpanan_indices = assigned_df[assigned_df['name'] == 'Simpanan'].index
    
    filled_count = 0
    
    for i in range(min(len(simpanan_indices), len(reserve_guests_list))):
        idx_to_replace = simpanan_indices[i]
        reserve_guest = reserve_guests_list[i]
        
        assigned_df.loc[idx_to_replace, 'name'] = reserve_guest.get('name')
        assigned_df.loc[idx_to_replace, 'menu'] = reserve_guest.get('menu', DEFAULT_MENU) 
        assigned_df.loc[idx_to_replace, 'gp_id'] = 999 
        assigned_df.loc[idx_to_replace, 'gp_name'] = 'Reserve'
        
        filled_count += 1
        
    print(f"Successfully filled {filled_count} vacant seats with reserve guests.")
    
    return assigned_df

def process_guest_files():
    """Process all guest files, assign seating, and fill vacant seats with reserves."""
    tempahan_folder = 'tempahan'
    
    if not os.path.exists(tempahan_folder):
        print(f"Error: Folder '{tempahan_folder}' not found. Please create it and place CSV files inside.")
        return pd.DataFrame()
        
    group_files = [f for f in os.listdir(tempahan_folder) if f.startswith('grp') and f.endswith('.csv')]
    
    group_files.sort(key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)
    
    guests = []
    global_guest_counter = 0 
    
    for file in group_files:
        file_path = os.path.join(tempahan_folder, file)
        group_df = read_csv_file(file_path)
        
        if group_df.empty:
            continue
            
        group_df = clean_guest_data(group_df)
        if group_df.empty:
            print(f"Warning: File {file} contained no valid guest records after cleaning.")
            continue
            
        gp_id_match = re.search(r'grp(\d+)', file)
        gp_id = int(gp_id_match.group(1)) if gp_id_match else 0
        gp_name_match = re.search(r'-(.*?)\.csv$', file)
        gp_name = gp_name_match.group(1).strip() if gp_name_match else "unknown"
        
        group_df['gp_id'] = gp_id
        group_df['gp_name'] = gp_name
        
        valid_guests = group_df.copy()
        valid_guests['original_order'] = range(global_guest_counter, global_guest_counter + len(valid_guests))
        global_guest_counter += len(valid_guests)
        
        guests.append(valid_guests)
    
    if not guests:
        print("No valid main guest data found.")
        return pd.DataFrame()
        
    guests_df = pd.concat(guests, ignore_index=True)
    
    assigned_seats_df = assign_seats(guests_df)
    
    reserve_guests_list = process_reserve_guests()
    
    final_guests_df = fill_vacant_seats(assigned_seats_df, reserve_guests_list)
    
    write_csv_file(final_guests_df, 'guest_seat.csv')
    
    return final_guests_df

if __name__ == '__main__':
    final_guests = process_guest_files()
    if not final_guests.empty:
        print("✅ Guest seating assignment completed. See guest_seat.csv for details.")
    else:
        print("❌ Guest seating assignment failed or no data processed.")
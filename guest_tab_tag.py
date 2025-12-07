import csv

def get_menu_color(menu):
    color_map = {
        'Daging': '#FF0000', # red
        'Ayam': '#008000',    # green
        'Ikan': '#0000FF',   # blue
        'Vegetarian': '#FFA500' # orange
    }
    return color_map.get(menu, 'unknown')

def main():
    input_file = 'all_seat.csv'
    
    # Create separate output files for each menu type
    output_files = {
        'Daging': 'daging.csv',
        'Ayam': 'ayam.csv',
        'Ikan': 'ikan.csv',
        'Vegetarian': 'vege.csv'
    }
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        # Create writers for each output file
        writers = {}
        for menu_type in output_files:
            outfile = output_files[menu_type]
            with open(outfile, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writers[menu_type] = writer
        
        # Process each row
        for row in reader:
            menu_type = row['menu']
            if menu_type in output_files:
                # Find the corresponding writer for this menu type
                for mt, writer in writers.items():
                    if mt == menu_type:
                        # Write to the appropriate file
                        with open(output_files[mt], 'a', newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=fieldnames)
                            writer.writerow(row)
                        break

if __name__ == '__main__':
    main()

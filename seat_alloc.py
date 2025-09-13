import csv
import re

def clean_txt(text):
    """
    Removes unprintable ASCII characters from a string using regex.
    """
    pattern = r'[^\x20-\x7E]+'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def get_menu(seat_number):
    """
    Determine menu type based on seat position within the table.
    Menu distribution:
        daging: 1-4 (4 seats)
        ayam: 5-7 (3 seats)
        ikan: 8 (1 seats)
    """
    pos = (seat_number - 1) % 8 + 1
    if 1 <= pos <= 4:
        return 'Daging'
    elif 5 <= pos <= 7:
        return 'Ayam'
    else:
        return 'Ikan'

def main():
    csv_file = "tempahan.csv"
    output_file = "guest_seat.csv"
    
    table_number = 13 # Table 1 - 12 premium pax
    seat_number = 1
    table_guest_count = 0

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['name', 'seat', 'table_number', 'menu', 'category'])
        writer.writeheader()

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                guest_name = row['Nama']
                guest_name = clean_txt(guest_name)
                value = row['Bil_tetamu'].strip()
                number_guest = int(value) if value else 1

                if table_guest_count + number_guest <= 8:
                    # Add to current table
                    for i in range(1, number_guest + 1):
                        if i == 1:
                            writer.writerow({
                                'name': f"{guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tetamu',
                                'menu': get_menu(seat_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Tetamu #{i}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tetamu',
                                'menu': get_menu(seat_number)
                            })
                        seat_number += 1
                    table_guest_count += number_guest

                elif table_guest_count < 8:
                    remaining = 8 - table_guest_count
                    for i in range(1, remaining + 1):
                        writer.writerow({
                            'name': f"Simpanan #{table_number}:{seat_number}",
                            'seat': str(seat_number),
                            'table_number': str(table_number),
                            'category': 'Tetamu',
                            'menu': ''
                        })
                        seat_number += 1
                    table_guest_count = 0
                    table_number += 1

                    # Process current guest in new table
                    for i in range(1, number_guest + 1):
                        if i == 1:
                            writer.writerow({
                                'name': f"{guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tetamu',
                                'menu': get_menu(seat_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Tetamu #{i}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tetamu',
                                'menu': get_menu(seat_number)
                            })
                        seat_number += 1
                    table_guest_count = number_guest

                else:
                    table_number += 1
                    table_guest_count = number_guest
                    for i in range(1, number_guest + 1):
                        if i == 1:
                            writer.writerow({
                                'name': f"{guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tajaan',
                                'menu': get_menu(seat_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Tetamu #{i} {guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number),
                                'category': 'Tajaan',
                                'menu': get_menu(seat_number)
                            })
                        seat_number += 1

        print(f"Total tables: {table_number}, Total guests: {seat_number}")

if __name__ == "__main__":
    main()

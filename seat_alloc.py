import csv
import re

def clean_txt(text):
    """
    Removes unprintable ASCII characters from a string using regex.
    """
    # Pattern matches any character NOT in the range of printable ASCII characters
    # (space to tilde, inclusive).
    pattern = r'[^\x20-\x7E]+'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def main():
    output_file = "guest_seat.csv"
    csv_file = "guest_merge.csv"
     
    table_number = 1
    seat_number = 1
    table_guest_count = 0

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['name', 'seat', 'table_number'])
        writer.writeheader()

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                guest_name = row['Nama']
                guest_name = clean_txt(guest_name)
                value = row['Jumlah Kehadiran'].strip()
                number_guest = int(value) if value else 1

                # Assign guest to table
                if table_guest_count + number_guest <= 10:
                    # Add to current table
                    for i in range(1, number_guest + 1):
                        if i == 1:
                            writer.writerow({
                                'name': f"{guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Ahli Keluarga #{i} {guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number)
                            })
                        seat_number += 1
                    table_guest_count += number_guest

                elif table_guest_count < 10:
                    # Fill remaining seats with Simpanan and start new table
                    remaining = 10 - table_guest_count
                    for i in range(1, remaining + 1):
                        writer.writerow({
                            'name': f"Simpanan #{table_number}:{seat_number}",
                            'seat': str(seat_number),
                            'table_number': str(table_number)
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
                                'table_number': str(table_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Ahli Keluarga #{i} {guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number)
                            })
                        seat_number += 1
                    table_guest_count = number_guest

                else:
                    # Start new table
                    table_number += 1
                    table_guest_count = number_guest
                    for i in range(1, number_guest + 1):
                        if i == 1:
                            writer.writerow({
                                'name': f"{guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number)
                            })
                        else:
                            writer.writerow({
                                'name': f"Ahli Keluarga #{i} {guest_name.title()}",
                                'seat': str(seat_number),
                                'table_number': str(table_number)
                            })
                        seat_number += 1

        # Print total tables
        print(f"Total tables: {table_number} Guests: {seat_number}")

if __name__ == "__main__":
    main()

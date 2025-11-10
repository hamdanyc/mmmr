import csv
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_guest_list():
    guests = []
    
    # Read CSV file
    with open('guest_seat.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # next(reader)  # Skip header row
        for row in reader:
            if row['name'].startswith('Ahli Keluarga'):
                continue
            guests.append({
                'name': row['name'],
                'table': row['table_number'],
                'seat': row['seat']
            })
    
    # Sort by name ascending
    guests.sort(key=lambda x: x['name'])
    
    # Create PDF
    c = canvas.Canvas("guest_list.pdf")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, 750, "Senarai Tetamu")
    
    # Add timestamp
    c.setFont("Helvetica", 10)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    c.drawString(150, 735, f"Berakhir pada: {timestamp}")
    
    # Add table headers
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, 700, "Tetamu")
    c.drawString(350, 700, "Meja")
    c.drawString(400, 700, "Siri")
    
    # Add guest data
    c.setFont("Helvetica", 12)
    y_position = 685
    for guest in guests:
        c.drawString(50, y_position, guest['name'])
        c.drawString(350, y_position, guest['table'])
        c.drawString(400, y_position, guest['seat'])
        y_position -= 15
        
        # Add new page if needed
        if y_position < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750
    
    c.save()

if __name__ == "__main__":
    generate_guest_list()

import csv
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def read_guest_list(csv_file):
    guests = {}
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table = row['table_number']
            name = row['name']
            seat = row['seat']
            menu = row['menu']
            if table not in guests:
                guests[table] = []
            guests[table].append((name, seat, menu))
    return guests

def generate_pdf(guests, output_file):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Header content
    title = Paragraph("Majlis Makan Malam RAFOC `25", styles['Heading1'])
    timestamp = Paragraph(f"Berakhir pada: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal'])
    
    # Add header content
    elements.append(title)
    elements.append(Spacer(1, 12))
    elements.append(timestamp)
    elements.append(Spacer(1, 24))

    table_count = 0  # Track number of tables added to current page

    # Add tables with page break prevention
    for table_number, entries in guests.items():
        # Table header
        header = Paragraph(f"Meja: {table_number}", styles['Heading2'])
        elements.append(header)
        elements.append(Spacer(1, 12))

        # Table data
        data = [["Tetamu", "Menu"]]
        for name, seat, menu in entries:
            data.append([name, menu])

        # Create and style the table
        table = Table(data, colWidths=(300, 50))  # Fixed to have 3 column widths
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#cccccc'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('GRID', (0, 0), (-1, -1), 1, '#dddddd'),
        ]))
        
        # Add table with page break prevention
        elements.append(table)
        elements.append(Spacer(1, 24))

        table_count += 1
        if table_count == 2:
            elements.append(PageBreak())
            table_count = 0

    doc.build(elements)

if __name__ == "__main__":
    guests = read_guest_list("guest_seat.csv")
    generate_pdf(guests, "guest_seat.pdf")

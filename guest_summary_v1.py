import pandas as pd
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

# Read CSV file
df = pd.read_csv('guest_seat.csv')

# Initialize summary dictionary
summary = {}

# Process each table
for table_num, group in df.groupby('table_number'):
    total_guests = len(group)
    gp_name = group['gp_name'].iloc[0]
    simpanan_count = group['name'].str.contains('simpanan', case=False).sum()
    daging_count = group['menu'].str.contains('Daging', case=False).sum()
    ayam_count = group['menu'].str.contains('Ayam', case=False).sum()
    ikan_count = group['menu'].str.contains('Ikan', case=False).sum()
    vege_count = group['menu'].str.contains('Vegetarian', case=False).sum()
    
    summary[table_num] = {
        'gp_name': gp_name,
        'total_guests': total_guests,
        'simpanan_count': simpanan_count,
        'daging_count': daging_count,
        'ayam_count': ayam_count,
        'ikan_count': ikan_count,
        'vege_count': vege_count
    }

# Convert to DataFrame
summary_df = pd.DataFrame.from_dict(summary, orient='index').reset_index()
summary_df.columns = ['Table Number', 'Table Name', 'Total Guests', 'Reserved', 'Daging', 'Ayam', 'Ikan', 'Vegetarian']

# Add adjusted total column (total guests minus simpanan count)
summary_df['Adjusted Total'] = summary_df['Total Guests'] - summary_df['Reserved']

# Add total row
total_row = {
    'Table Number': 'Total',
    'Total Guests': summary_df['Total Guests'].sum(),
    'Reserved': summary_df['Reserved'].sum(),
    'Adjusted Total': summary_df['Adjusted Total'].sum(),
    'Daging': summary_df['Daging'].sum(),
    'Ayam': summary_df['Ayam'].sum(),
    'Ikan': summary_df['Ikan'].sum(),
    'Vegetarian': summary_df['Vegetarian'].sum()
}
summary_df = pd.concat([summary_df, pd.DataFrame([total_row])], ignore_index=True)

# Create PDF document
pdf = SimpleDocTemplate("table_summary.pdf", pagesize=letter)
elements = []

# Add title
styles = getSampleStyleSheet()
title_style = styles['Heading1']
title = Paragraph("Tables Summary", title_style)
timestamp = Paragraph(f"Berakhir pada: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}", styles['Normal'])
elements.append(title)
elements.append(Spacer(1, 12))
elements.append(timestamp)
elements.append(Spacer(1, 24))

# Define a style for wrapping column headers
header_style = styles['Normal']
header_style.fontSize = 8 # Smaller font
header_style.alignment = TA_CENTER
header_style.leading = 9 # Smaller line spacing

# Manually insert line breaks for long titles
header_titles = summary_df.columns.tolist()
# Apply manual breaks for fitting in small columns
header_titles[0] = 'Table<br/>Number'
header_titles[1] = 'Table<br/>Name'
header_titles[2] = 'Total<br/>Guests'
header_titles[8] = 'Adjusted<br/>Total'

# Convert column names to Paragraph objects for wrapping
header_row = [Paragraph(name, header_style) for name in header_titles]

# Convert DataFrame to list of lists for table
data = [header_row] + summary_df.values.tolist()

# Define column widths (in points: 72 points = 1 inch)
# Total width is approximately 550 points (around 7.6 inches for a letter page)
colWidths = [50, 150, 50, 50, 50, 50, 50, 50, 50] # Total: 550 points. Table Name set to 150 points.

# Create table and apply styling
table = Table(data, colWidths=colWidths) # Pass the column widths here
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), '#cccccc'),
    ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), '#ffffff'),
    ('GRID', (0, 0), (-1, -1), 1, '#000000'),
]))

elements.append(table)

# Build PDF
pdf.build(elements)

print("Analysis complete. Results written to table_summary.pdf")
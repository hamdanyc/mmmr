import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set page title and config
st.set_page_config(page_title="Majlis Makan Malam RAFOC 2025", layout="wide")

# --- Dummy Data Initialization ---
# Assuming these dataframes are loaded from your CSV files.
try:
    tetamu_df = pd.read_csv("guest_seat.csv")
    tajaan_df = pd.read_csv("tajaan.csv")
    tempah_df = pd.read_csv("tempahan.csv")
except FileNotFoundError:
    st.warning("One or more CSV files not found. Using dummy data.")
    # Dummy data for demonstration
    data = {'table_number': list(range(1, 50)), 'name': [f'Guest {i}' for i in range(1, 50)], 'menu': ['Daging', 'Ayam'] * 24 + ['Ikan']}
    tetamu_df = pd.DataFrame(data)
    tajaan_df = pd.DataFrame({'Jumlah': [25000, 30000]})
    tempah_df = pd.DataFrame({'Nama': [f'Wakil {chr(65+i)}' for i in range(49)]})
# --- End Dummy Data Initialization ---

# Countdown to event
event_date = datetime(2025, 12, 14)
now = datetime.now()
delta = event_date - now
if delta.total_seconds() < 0:
    countdown_text = "Event has started!"
else:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown_text = f"{days} days: {hours} hours: {minutes} minutes: {seconds} seconds"

# 1. Table Layout Grid (Responsive)
st.markdown("<h2 style='text-align: right; color: red; font-weight: bold'</h2>"f"⏳ Countdown: {countdown_text}", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: blue; font-weight: bold'>Majlis Makan Malam RAFOC | 14 Dis 2025</h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: blue; font-weight: bold'>Status Tempahan Meja | Tajaan | Tetamu</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00008B;'>🗺️ Tempahan Meja</h3>", unsafe_allow_html=True)

# Get wakil names in the same order as booked tables
wakil_names = tempah_df['Nama'].tolist()
booked_tables = tetamu_df['table_number'].astype(int).tolist()

# --- NEW CODE BLOCK FOR HEAD TABLES ---
# --- NEW CODE BLOCK FOR HEAD TABLES ---
head_boxes_html = """
<style>
    /* Container to hold the two head tables side-by-side and center them relative to the grid */
    .head-table-container {
        display: flex; 
        justify-content: center; /* This centers the boxes within the 800px width */
        gap: 20px; /* Increased space between the two boxes for a cleaner look */
        margin: 0 auto 5px auto; /* Center the container itself and add space below */
        max-width: 800px; /* Match the max-width of the main grid */
    }

    .head-box {
        background-color: #FF9900; /* Orange color */
        border: 1px solid #444;
        color: white;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 50px; 
        /* Key Change: Set a specific, smaller width instead of filling the container */
        width: 250px; 
        /* Removed flex: 1 to prevent them from taking up all available space */
    }
</style>
<div class="head-table-container">
    <div class="head-box">Diraja 1</div>
    <div class="head-box">Diraja 2</div>
</div>
"""

# Display the head tables before the main grid
st.markdown(head_boxes_html, unsafe_allow_html=True)
# --- END NEW CODE BLOCK ---


# Generate responsive grid HTML (ORIGINAL CODE BELOW, MODIFIED SLIGHTLY FOR CLEANER STYLE TAG)
grid_html = """
<style>
    /* MODIFIED: Removed margin: 0 auto; and max-width: 800px; from .table-grid as 
       the structure is now separated, but keeping it for safety */
    .table-grid {
        display: grid;
        grid-template-columns: repeat(9, 1fr);
        grid-template-rows: repeat(7, 1fr);
        gap: 5px;
        margin: 0 auto;
        max-width: 800px;
    }
    .table-cell {
        border: 1px solid #444;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: black;
        padding: 10px;
        text-align: center;
        flex-direction: column;
        aspect-ratio: 1 / 1; /* Added for square cells */
    }
    .booked { background-color: #00FFFF; } /* Aqua */
    .vacant { background-color: #778899; } /* Grey */
    @media (max-width: 600px) {
        .table-cell {
            font-size: 10px;
            padding: 5px;
        }
    }
</style>
<div class="table-grid">
"""

# Create 7 rows with 7 columns each (49 tables total)
wakil_index = 0
for row in range(7):
    for col in range(9):
        table_number = row * 9 + col + 1 
        table_id = f"R{table_number}"
        
        # If this table is in the booked tables list and we still have wakil names
        if table_number in booked_tables and wakil_index < len(wakil_names):
            grid_html += f'<div class="table-cell booked">{table_id} | {wakil_names[wakil_index]}</div>'
            wakil_index += 1
        else:
            # Added logic check: If table is booked but no name is available, 
            # or if it's genuinely vacant.
            if table_number in booked_tables and wakil_index >= len(wakil_names):
                grid_html += f'<div class="table-cell booked">{table_id} | No Wakil</div>'
            else:
                grid_html += f'<div class="table-cell vacant">{table_id}</div>'

grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

st.markdown("<h3 style='color: #00008B;'>💰 Tajaan & 👥 Tetamu</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Tajaan Gauge (Unchanged)
with col1:
    total_collections = tajaan_df['Jumlah'].sum()
    collection_target = 100000
    percentage = (total_collections / collection_target) * 100 if collection_target > 0 else 0

    fig_collections = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 30], 'color': "red"},
                {'range': [30, 80], 'color': "gold"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': percentage
            }
        }
    ))
    fig_collections.update_layout(height=150, margin=dict(l=0, r=0, b=0, t=30, pad=0))
    st.plotly_chart(fig_collections, use_container_width=True)
    st.info(f"Sasaran: RM {collection_target}")
    st.metric(label="Tajaan", value=f"RM {total_collections:,.2f}")

# Tetamu Gauge (Unchanged)
with col2:
    total_simpanan = tetamu_df['name'].str.contains('simpanan', case=False).sum()
    total_guests = len(tetamu_df) - total_simpanan
    guests_target = 504
    guests_percentage = (total_guests / guests_target) * 100 if guests_target > 0 else 0

    fig_guests = go.Figure(go.Indicator(
        mode="gauge+number",
        value=guests_percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 30], 'color': "red"},
                {'range': [30, 80], 'color': "gold"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': guests_percentage
            }
        }
    ))
    fig_guests.update_layout(height=150, margin=dict(l=0, r=0, b=0, t=30, pad=0))
    st.plotly_chart(fig_guests, use_container_width=True)
    st.info(f"Sasaran: {guests_target} Tetamu")
    st.metric(label="Tetamu", value=total_guests)

# Menu Preferences (Unchanged)
with col3:
    st.markdown("<h3 style='color: #00008B;'>🍽️ Menu Pilihan</h3>", unsafe_allow_html=True)
    menu_counts = tetamu_df['menu'].value_counts()
    menu_icons = {
        "Daging": "🥩",
        "Ayam": "🍗",
        "Ikan": "🐟",
        "Vegetarian": "🥬"
    }
    menu_display = "\n".join([f"<span style='font-size: 20px; color: #006400; font-weight: bold;'>{menu_icons.get(menu, '❓')} <strong>{menu}</strong>: {count}</span>" for menu, count in menu_counts.items()])
    st.markdown(menu_display, unsafe_allow_html=True)

# Apply dark red and blue theme and responsive styles (Unchanged)
st.markdown(
    """
    <style>
    body {
        background-color: blue;
        color: #f5f5f5;
        font-family: Arial, sans-serif;
    }
    .stMetricValue {
        color: #007bff;
    }
    .stMetricLabel {
        color: #ff4b4b;
    }
    .stText, .stMarkdown {
        color: #f5f5f5;
    }
    h1, h2, h3, h4, h5, h6 {
        font-size: 24px !important;
        color: #8B0000;
    }
    .stButton>button {
        background-color: #8B0000;
        color: white;
    }
    .stTextInput>div>div>input {
        color: #8B0000;
        border-color: #00008B;
    }
    @media (max-width: 600px) {
        h1 {
            font-size: 20px !important;
            text-align: center;
        }
        h3 {
            font-size: 18px !important;
        }
        .stMetric {
            font-size: 14px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set page title and config
st.set_page_config(page_title="Majlis Makan Malam RAFOC 2025", layout="wide")

# Load data
tetamu_df = pd.read_csv("tetamu.csv")
tajaan_df = pd.read_csv("tajaan.csv")

# 1. Table Layout Grid (Responsive)
st.markdown("<h1 style='text-align: center; color: #8B0000;'>Majlis Makan Malam RAFOC 2025</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #00008B;'>🗺️ Tempahan Meja</h3>", unsafe_allow_html=True)

# Filter MR tables only
mr_tables = tetamu_df['No_Meja'].astype(int)
booked_tables = set(mr_tables)

# Generate responsive grid with 8 rows and 6 columns
grid_html = """
<style>
    .table-grid {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        grid-template-rows: repeat(8, 1fr);
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

# Create 8 rows with 6 columns each (48 tables total)
for row in range(10):
    for col in range(6):
        table_number = row * 6 + col + 1 
        table_id = f"R{table_number}"
        if table_number in booked_tables:
            grid_html += f'<div class="table-cell booked">{table_id}</div>'
        else:
            grid_html += f'<div class="table-cell vacant">{table_id}</div>'

grid_html += "</div>"
st.markdown(grid_html, unsafe_allow_html=True)

# 2. Tajaan vs Target with Gauge Meter
st.markdown("<h3 style='color: #00008B;'>💰 Tajaan</h3>", unsafe_allow_html=True)
total_collections = tajaan_df['Jumlah'].sum()
collection_target = 800000
percentage = (total_collections / collection_target) * 100 if collection_target > 0 else 0

# Create gauge chart for collections
fig_collections = go.Figure(go.Indicator(
    mode="gauge+number",
    value=percentage,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Collections Progress"},
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

# Reduce chart size
st.plotly_chart(fig_collections, use_container_width=True)

st.info(f"Sasaran: RM {collection_target}")
st.metric(label="Tajaan", value=f"RM {total_collections:,.2f}")

# 3. Tetamu with Gauge Meter
st.markdown("<h3 style='color: #00008B;'>👥 Tetamu</h3>", unsafe_allow_html=True)
total_guests = len(tetamu_df)
guests_target = 600
guests_percentage = (total_guests / guests_target) * 100 if guests_target > 0 else 0

# Create gauge chart for guests
fig_guests = go.Figure(go.Indicator(
    mode="gauge+number",
    value=guests_percentage,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Guests Progress"},
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

# Reduce chart size
st.plotly_chart(fig_guests, use_container_width=True)

st.info(f"Sasaran: {guests_target} Tetamu")
st.metric(label="Tetamu", value=total_guests)

# 4. Menu Preferences (Text-based with icons)
st.markdown("<h3 style='color: #00008B;'>🍽️ Menu Pilihan</h3>", unsafe_allow_html=True)
menu_counts = tetamu_df['Menu'].value_counts()
menu_icons = {
    "Daging": "🥩",
    "Ayam": "🍗",
    "Ikan": "🐟",
    "Vegetarian": "🥬"
}
menu_display = "\n".join([f"<span style='font-size: 20px; color: #006400; font-weight: bold;'>{menu_icons.get(menu, '❓')} <strong>{menu}</strong>: {count}</span>" for menu, count in menu_counts.items()])
st.markdown(menu_display, unsafe_allow_html=True)

# Apply dark red and blue theme and responsive styles
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
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

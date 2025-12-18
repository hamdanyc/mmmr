import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="RAFOC 2025 Guest List", layout="centered")

# --- DATABASE CONNECTION ---
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=600)
def load_data():
    # No URL needed here anymore! It pulls from secrets automatically.
    df = conn.read() 
    df = df.rename(columns={
        'name': 'Nama', 
        'table_number': 'Meja', 
        'menu': 'Menu', 
        'gp_name': 'Kluster'
    })
    return df[['Nama', 'Meja', 'Menu', 'Kluster']]

df = load_data()

# --- UI ELEMENTS ---
st.title("Majlis Makan Malam RAFOC 2025")

# Countdown to event
event_date = datetime(2025, 12, 14, 20, 0, 0)
now = datetime.now()
delta = event_date - now

if delta.total_seconds() < 0:
    countdown_text = "Acara telah bermula!"
else:
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    countdown_text = f"{days} hari, {hours} jam, {minutes} minit"

st.subheader("WTC 14 Dis 2025")
st.info(f"Countdown: {countdown_text}")

# --- SEARCH LOGIC ---
column = st.selectbox("Saring Mengikut", df.columns)
query = st.text_input("Carian Nama atau No. Meja")

if query:
    # Filter the dataframe based on search
    results = df[df[column].astype(str).str.contains(query, case=False, na=False)]
else:
    results = df

st.dataframe(results, use_container_width=True, hide_index=True)
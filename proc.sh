echo "seat allocation -- start"
uv run seat_alloc.py
sed -i 's/Tudm/TUDM/g;s/Mmu/MMU/g;s/Tldm/TLDM/g;s/Apmm/APMM/g;s/Jhev/JHEV/g;s/Pvatm/PVATM/g;s/Ramd/RAMD/g;s/Pgb/PGB/g;s/Kagat/KAGAT/g;s/Ugat/UGAT/g;s/Kko/KKO/g;s/Ppp/PPP/g;s/Ydp/YDP/g;s/Adc/ADC/g;s/Hs/HS/g' guest_seat.csv
uv run guest_seat_pdf.py
uv run guest_seat_analyzer.py
uv run guest_list.py
echo "seat allocation -- done"

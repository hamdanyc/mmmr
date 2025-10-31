echo "seat allocation -- start"
uv run guest_seat_assign.py
sed -i 's/Tudm/TUDM/g;s/Mmu/MMU/g;s/Tldm/TLDM/g;s/Apmm/APMM/g;s/Jhev/JHEV/g;s/Pvatm/PVATM/g;s/Ramd/RAMD/g;s/Pgb/PGB/g;s/Kagat/KAGAT/g;s/Ugat/UGAT/g;s/Kko/KKO/g;s/Ppp/PPP/g;s/Ydp/YDP/g;s/Adc/ADC/g;s/Hs/HS/g' guest_seat.csv
uv run guest_seat_pdf.py
uv run guest_summary.py
uv run guest_list.py
uv run guest_tab_tag.py
echo "seat allocation -- done"

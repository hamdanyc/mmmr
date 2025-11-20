echo "seat allocation -- start"
uv run guest_seat_gem.py
# sed -E 's/\<[[:alpha:]]{3,}\>/\U&/g'
sed -i 's/Pat/PAT/g;s/Ptd/PTD/g;s/Ptl/PTL/g;s/Ptu/PTU/g;s/Tudm/TUDM/g;s/Mmu/MMU/g;s/Tldm/TLDM/g;s/Apmm/APMM/g;s/diraja/Diraja/g;
    s/Othman-Yaakob/Othman Yaakob Lt Kol (B)/g;s/Nawawi-Desa/Dato Nawawi Desa Lt Kol (B)/g;s/murthy/Dato Dr Murthy Mej (B)/g;
    s/Jhev/JHEV/g;s/Pvatm/PVATM/g;s/Ramd/RAMD/g;s/Pgb/PGB/g;s/Kagat/KAGAT/g;s/rma-sandhurst/RMA Sandhurst/g;s/dmhk/DMHK/g;
    s/Ramli-Kinta/Ramli Kinta Lt Kol (B)/g;s/Ugat/UGAT/g;s/Pernama/PERNAMA/g;s/Dymm/DYMM/g;s/Yb/YB/g;s/Adc/ADC/g;s/Hs/HS/g' guest_seat.csv
uv run guest_seat_pdf.py
uv run guest_summary.py
uv run guest_list.py
uv run guest_tab_tag.py
echo "seat allocation -- done"

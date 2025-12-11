#!/bin/bash
echo "seat allocation -- start"
uv run guest_seat_gem.py
# sed -E 's/\<[[:alpha:]]{3,}\>/\U&/gI'
sed -i '
    s/Pat/PAT/gI;s/Ptd/PTD/gI;s/Ptl/PTL/gI;s/rose/Rose /gI;s/Tudm/TUDM/gI;s/Mmu/MMU/gI;s/Tldm/TLDM/gI;s/khas/Khas /gI;s/diraja/Diraja/gI;
    s/Othman-Yaakob/Othman Yaakob Lt Kol (B)/gI;s/Nawawi-Desa/Dato Nawawi Desa Lt Kol (B)/gI;s/pvrad/The Gunners/gI;
    s/murthy/Mej Datuk M.S. Murthi/gI;s/bhc/Black Hackle Club/gI;s/abdullah-ltj/Abdullah Lt Jen (B)/gI;
    s/Jhev/JHEV/gI;s/Pvatm/PVATM/gI;s/Ramd/RAMD/gI;s/Pgb/PGB/gI;s/nv/NV/gI;s/rma-sandhurst/RMA Sandhurst/gI;s/dmhk/DMHK/gI;
    s/Ramli-Kinta/Ramli Kinta Lt Kol (B)/gI;s/ssc26l/SSC 26 TLDM/gI;s/Pernama/PERNAMA/gI;s/Dymm/DYMM/gI;s/Yb/YB/gI;s/Adc/ADC/gI;s/Hs/HS/gI
' guest_seat.csv
# This line is modified to use standard grouping and echo for a newline
(cat diraja.csv; echo; tail -n +2 guest_seat.csv) > all_seat.csv
uv run guest_seat_pdf.py
uv run guest_summary_v1.py
uv run guest_list.py
uv run guest_tab_tag.py
# append extra data to files
cat rs99.csv >> ayam.csv;cat rs99.csv >> daging.csv;cat rs99.csv >> ikan.csv
echo "seat allocation -- done"
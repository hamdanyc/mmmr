# Event Seat Allocation System

This system is designed to allocate seats for guests based on a CSV file (`tempahan.csv`) and generate a final seating plan in `guest_seat.csv`. It also produces a PDF of the seating arrangement and analyzes the data.

## 🚀 How to Use

1. **Prepare the Input File**
   - Place your group booking in a CSV file named `tempahan.csv`.
   - `tempahan.csv` and `guest_seat.csv` are for the dashboard.
   - The CSV must have the following columns:
     - `Nama`: Guest's name.
     - `Bil_tetamu`: Number of guests (default is 1 if empty).
   - Prepare the respective group booking in the `folder: tempahan`. Data elements:
     - Name, Menu ([Daging], Ayam, Ikan, Vege)

2. **Run the Script**
   Execute the `proc.sh` script:
   ```bash
   ./proc.sh
   ```

   This will:
   - Generate a `guest_seat.csv` file with the seating plan.
   - Generate a PDF of the seating plan and the guests' list.
   - Generate the table tag according to the Menu ([Daging], Ayam, Ikan, Vege)

3. **Output Files**
   - `guest_seat.csv`: Final seating plan with guest names, seat numbers, table numbers, and menu types.
   - `guest_seat.pdf`: PDF version of the seating plan.
   - `guest_list.csv`: Summary of the guest list and seating distribution.
   - `daging.csv; ayam.csv; ikan.csv; vege.csv`: tag for menu.

## 🧠 Notes

- The script uses a specific menu distribution based on seat position:
  - **Daging**: Seats 1-4
  - **Ayam**: Seats 5-7
  - **Ikan**: Seat 8
- If a guest brings more than one person, additional guests are labeled as "Tetamu #n".
- The system automatically fills empty seats with "Simpanan" entries to ensure tables are complete.
- Guest names are capitalized for consistency.

## 🛠️ Troubleshooting

- If you encounter permission issues with `proc.sh`, make it executable:
  ```bash
  chmod +x proc.sh
  ```
- If `sed` fails on macOS, install GNU `sed` via Homebrew:
  ```bash
  brew install gnu-sed
  ```

## 📌 File Structure

- `proc.sh`: Main script to run the entire process.
- `guest_seat_assign.py`: Assign seats based on the reservation.
- `guest_seat_pdf.py`: Generates a PDF of the seating plan.
- `guest_summary.py`: Summary of the seating arrangement.
- `guest_list.py`: Generates a summary guest list.


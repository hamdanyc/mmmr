# Seat Allocation Instructions

This document outlines the steps to follow to execute the seat allocation process as defined in the `proc.sh` script.

## Pre-Execution Steps

1.  **Ensure Dependencies:** Verify that all necessary files are present in the expected locations. Specifically:
    *   `tempahan.csv` (the input CSV file)
    *   `guest_seat.csv` (the output CSV file)
    *   `guest_seat_pdf.py` (the Python script to generate a PDF report)
    *   `guest_seat_analyzer.py` (the Python script for analysis)
    *   `guest_list.py` (the Python script for generating a guest list)

## Execution Steps

1.  **Run `proc.sh`:** Execute the `proc.sh` script using the command: `proc.sh`
2.  **Monitor Output:** Observe the output of the script in the terminal. The script will perform the following actions:
    *   Print a starting message: "seat allocation -- start"
    *   Run the `guest_seat.py` script.
    *   Use `sed` to modify the `guest_seat.csv` file.
    *   Run the `guest_seat_pdf.py` script to generate a PDF report.
    *   Run the `guest_seat_analyzer.py` script for analysis.
    *   Run the `guest_list.py` script to generate a guest list.
    *   Print a completion message: "seat allocation -- done"

## Important Notes

*   The script assumes that `tempahan.csv` is in the same directory as `proc.sh`.
*   The script uses `sed` to modify the `guest_seat.csv` file.  This is a critical step.
*   The script handles seat allocation based on the data in `tempahan.csv`.
*   The script generates a PDF report using `guest_seat_pdf.py`.
*   The script performs analysis using `guest_seat_analyzer.py`.
*   The script generates a guest list using `guest_list.py`.

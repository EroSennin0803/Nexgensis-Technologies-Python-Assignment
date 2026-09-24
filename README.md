# FastBox Delivery Simulator

A Python-based logistics simulator that processes delivery data, assigns packages to the nearest agents using Euclidean distance, and generates a performance report.

## Routing Logic & Assumptions
* **Dynamic Location Routing:** After completing a delivery, an agent's starting location dynamically updates to the drop-off destination. Subsequent dispatch distances are calculated from this new location.
* **Top Performer Criteria:** The "best agent" is determined by finding the active agent (completed > 0 deliveries) with the lowest efficiency score (traveling the least distance per package). 

## Bonus Features Included
* **CSV Export:** The script automatically exports the top-performing agent's statistics to a `top_performer.csv` file.

## How to Run
1. Ensure Python 3.x is installed.
2. Verify `data.json` is in the same directory as the script.
3. Run the simulation:
   ```bash
   a.py

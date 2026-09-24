import json
import math
import csv

def main():

    # 1. Read and parse the JSON file manually
    try:
        # Load the input data containing coordinates for warehouses, agents, and packages
        with open('data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: 'data.json' not found. Please ensure the file exists in the directory.")
        return

    # Extract warehouses and packages lists from the parsed JSON
    warehouses = data.get("warehouses", {})
    packages = data.get("packages", [])
    
    # Initialize a tracking dictionary to monitor each agent's state throughout the day
    agents_tracker = {}
    for a_id, coords in data.get("agents", {}).items():
        agents_tracker[a_id] = {
            "location": coords,          # Current [x, y] coordinates
            "packages_delivered": 0,     # Total count of successful deliveries
            "total_distance": 0.0        # Cumulative distance traveled
        }

    # 2 & 3. Simulate delivery assignments and calculate distances
    # ASSUMPTION: I am assuming that the location of delivery agent is dynamic, meaning after completing a delivery, the location of agent would be location of where the package got delivered
    for pkg in packages:
        w_id = pkg["warehouse"]
        w_loc = warehouses[w_id]
        d_loc = pkg["destination"]
        
        best_agent_id = None
        min_dist_to_warehouse = float('inf')
        
        # Find the agent currently closest to the package's originating warehouse
        # math.dist is an inbuilt funtion which uses eucledian distance to find distance between two points.
        for a_id, a_data in agents_tracker.items():
            dist = math.dist(a_data["location"], w_loc)
            if dist < min_dist_to_warehouse:
                min_dist_to_warehouse = dist
                best_agent_id = a_id

        # Calculate the actual delivery distance (Warehouse to Destination)
        delivery_dist = math.dist(w_loc, d_loc)
        
        # Total trip is the approach distance plus the delivery distance
        total_trip_dist = min_dist_to_warehouse + delivery_dist
        
        # Update the winning agent's performance metrics
        agents_tracker[best_agent_id]["total_distance"] += total_trip_dist
        agents_tracker[best_agent_id]["packages_delivered"] += 1
        
        # Update the agent's location to the drop-off point for the next loop iteration
        agents_tracker[best_agent_id]["location"] = d_loc 

    # 4. Generate the performance report
    report = {}
    for a_id, a_data in agents_tracker.items():
        delivered = a_data["packages_delivered"]
        dist = a_data["total_distance"]
        
        # Calculate efficiency (Total Distance / Packages Delivered)
        # Avoid division by zero for agents who made no deliveries
        efficiency = round(dist / delivered, 2) if delivered > 0 else 0.0
        
        report[a_id] = {
            "packages_delivered": delivered,
            "total_distance": round(dist, 2),
            "efficiency": efficiency
        }

    # Determine the "best_agent"
    # LOGIC: The best agent is the one with the lowest efficiency score (least distance traveled per package).
    # Filter out inactive agents (0 deliveries) so they do not win by default with a 0.0 score.
    active_agents = {a_id: stats for a_id, stats in report.items() if stats["packages_delivered"] > 0}
    
    if active_agents:
        # Find the active agent with the minimum efficiency value
        best_agent = min(active_agents.keys(), key=lambda k: active_agents[k]["efficiency"])
    else:
        best_agent = None
        
    report["best_agent"] = best_agent

    # 5. Save the summary report to a JSON file
    with open('report.json', 'w') as out_file:
        json.dump(report, out_file, indent=4)
        
    print("\nSimulation complete. Results saved to 'report.json'.")
    
    # BONUS: Export the top performing agent's data to a CSV file
    if best_agent:
        best_agent_stats = report[best_agent]
        
        with open('top_performer.csv', 'w', newline='') as csv_file:
            # Define the column headers for the CSV
            fieldnames = ['Agent_ID', 'Packages_Delivered', 'Total_Distance', 'Efficiency']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write the header row followed by the top performer's actual data
            writer.writeheader()
            writer.writerow({
                'Agent_ID': best_agent,
                'Packages_Delivered': best_agent_stats['packages_delivered'],
                'Total_Distance': best_agent_stats['total_distance'],
                'Efficiency': best_agent_stats['efficiency']
            })
            
        print("Top performer exported to 'top_performer.csv'.")
    else:
        print("No active agents to export to CSV.")

if __name__ == "__main__":
    main()
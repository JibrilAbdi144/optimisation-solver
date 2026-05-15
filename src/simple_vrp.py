from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import random
import math
import numpy as np

def create_data():
    # 1. Simple Data Generation
    num_vehicles = 4
    num_customers = 20
    depot = 0
    
    # Generate random coordinates
    coords = [(0.,0.)] # Depot
    for _ in range(num_customers):
        #coords.append((np.random.uniform(0, 100), np.random.uniform(0, 100)))
        coords.append((np.random.uniform(0, 100), np.random.uniform(0, 100)))
    
    # Build Distance Matrix
    n = len(coords)
    #dist_matrix = [[0.0]*n for _ in range(n)]
    dist_matrix = [[0. for _ in range(n)] for _ in range(n) ]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist_matrix[i][j] = math.hypot(coords[i][0]-coords[j][0], coords[i][1]-coords[j][1])
    
    # 2. THE KEY: Hardcoded Constraints for Balance
    # Total demand = 20. 
    # We have 4 vehicles. 
    # If we set capacity to 5, each vehicle MUST take exactly 5.
    demands = [0] + [1] * num_customers
    capacities = [5] * num_vehicles  # 4 * 5 = 20. Perfect fit.
    
    return {
        'distance_matrix': dist_matrix,
        'demands': demands,
        'vehicle_capacities': capacities,
        'num_vehicles': num_vehicles,
        'depot': depot
    }

def main():
    data = create_data()
    
    # Create Manager and Routing Model
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), 
                                           data['num_vehicles'], 
                                           data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    # --- Distance Callback ---
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node]) # Cast to int for OR-Tools

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # --- Distance Dimension (Optional, but good for logging) ---
    routing.AddDimension(transit_callback_index, 0, 1000, True, "Distance")

    # # --- CAPACITY CONSTRAINT (THE MAGIC PART) ---
    # def demand_callback(from_index, to_index):
    #     from_node = manager.IndexToNode(from_index)
    #     return data['demands'][from_node]

    # demand_callback_index = routing.RegisterTransitCallback(demand_callback)
    
    # # This line FORCES the solver to respect the capacity limits
    # routing.AddDimensionWithVehicleCapacity(
    #     demand_callback_index,
    #     0,
    #     data['vehicle_capacities'],
    #     True,
    #     "Capacity"
    # )

    # --- Search Parameters ---
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    # search_parameters.local_search_metaheuristic = (
    #     routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    # )
    search_parameters.time_limit.FromSeconds(5)

    # --- Solve ---
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        print("\n--- SOLUTION FOUND ---")
        for v in range(data['num_vehicles']):
            index = routing.Start(v)
            route = []
            capacity_used = 0
            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                capacity_used += data['demands'][node]
                index = solution.Value(routing.NextVar(index))
            
            # Get total distance for this vehicle
            dist_dim = routing.GetDimensionOrDie("Distance")
            total_dist = solution.Value(dist_dim.CumulVar(routing.End(v)))
            
            print(f"Vehicle {v}: {route} | Distance: {total_dist:.1f} | Load: {capacity_used}/5")
    else:
        print("No solution found!")

if __name__ == '__main__':
    main()
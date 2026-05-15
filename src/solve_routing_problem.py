from ortools.constraint_solver import routing_enums_pb2, pywrapcp

def solveTransportProblem(data_model: dict):

    routing_index_manager = pywrapcp.RoutingIndexManager(
        len(data_model["distance_matrix"]),
        data_model["num_vehicles"],
        data_model["depot"]
    )
    routing_model = pywrapcp.RoutingModel(routing_index_manager)

    def distanceCallback(from_index, to_index):
        from_node = routing_index_manager.IndexToNode(from_index)
        to_node = routing_index_manager.IndexToNode(to_index)
        return data_model["distance_matrix"][from_node][to_node]
    distance_callback_index = routing_model.RegisterTransitCallback(distanceCallback)
    routing_model.SetArcCostEvaluatorOfAllVehicles(distance_callback_index)
    dimension_name = "Distance"
    routing_model.AddDimension(
        distance_callback_index,
        0,
        300000,
        True,
        dimension_name
    )
    distance_dimension = routing_model.GetDimensionOrDie(dimension_name=dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(1000)

    # def capacityCallback(from_index, to_index):
    #     from_node = routing_index_manager.IndexToNode(from_index)
    #     return data_model["demands"][from_node]
    # capacity_callback_index = routing_model.RegisterTransitCallback(capacityCallback)
    # #Update the following for case where vehicles have different capacities
    # routing_model.AddDimension(
    #     capacity_callback_index,
    #     0,
    #     data_model["vehicle_capacities"][0],
    #     True,
    #     "Capacity"
    # )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing_model.SolveWithParameters(search_parameters)

    if solution:
        #print(solution.ObjectiveValue())
        total_distance = 0
        routes = []
        for vehicle_id in range(data_model["num_vehicles"]):
            vehicle_index = routing_index_manager.GetStartIndex(vehicle=vehicle_id)
            vehicle_route = []
            route_load = 0
            route_distance = 0
            while not routing_model.IsEnd(vehicle_index):
                vehicle_node = routing_index_manager.IndexToNode(vehicle_index)
                vehicle_route.append(vehicle_node)
                previous_vehicle_index = vehicle_index
                if vehicle_index != 0:
                    route_load += data_model["demands"][vehicle_node]
                vehicle_index = solution.Value(routing_model.NextVar(vehicle_index))
                route_distance += routing_model.GetArcCostForVehicle(
                    previous_vehicle_index, vehicle_index, vehicle_id
                )
            vehicle_route.append(routing_index_manager.IndexToNode(vehicle_index))
            total_distance += route_distance
            routes.append(vehicle_route)
                
            #print(f"Route of Vehicle {vehicle_id}: {vehicle_route}\nVehicle {vehicle_id} Route Load: {route_load}\nVehicle Route Distance: {route_distance}")
        #print(f"Total Distance: {total_distance}")
        return routes
    else:
        raise Exception("Error: Solution does not exist")

    #return solution

def solveTransportProblemExample(data: dict):
    """Entry point of the program."""

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = "Distance"
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name,
    )
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    def demandCallback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        #to_node = manager.IndexToNode(to_index)
        return data["demands"][from_node]
    
    demand_callback_index = routing.RegisterTransitCallback(demandCallback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data["vehicle_capacities"],
        True,
        "Capacity"
    )

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        for vehicle_id in range(data["num_vehicles"]):
            vehicle_index = manager.GetStartIndex(vehicle=vehicle_id)
            vehicle_route = []
            while not routing.IsEnd(vehicle_index):
                vehicle_route.append(manager.IndexToNode(vehicle_index))
                vehicle_index = solution.Value(routing.NextVar(vehicle_index))
            print(f"Route for Vehicle {vehicle_id}: {vehicle_route}")
    else:
        print("No solution found !")

    return solution
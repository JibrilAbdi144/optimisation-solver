import numpy as np

from src.london_locations import generateCustomerCoords
from src.data_generator import generateDistanceMatrix, formatDataForVRPSolver, printDistanceMatrix
from src.solve_routing_problem import solveTransportProblem, solveTransportProblemExample

if __name__ == "__main__":
    SEED_VALUE = 42
    np.random.seed(SEED_VALUE)
    
    CHARING_CROSS_DEPOT = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }

    customers = generateCustomerCoords(customer_number=10)

    #distance_matrix = generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)
    distance_matrix = [[int(value) for value in row] for row in generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)]
            

    data = formatDataForVRPSolver(distance_matrix=distance_matrix, customer_demands=([0] + [1 for customer in customers]))

    # print("This is my distance matrix")
    # printDistanceMatrix(distance_matrix=data["distance_matrix"])

    # print(f"Customer demands: {data["demands"]}\nVehicle Capacities: {data["vehicle_capacities"]}\nVehicle Number: {data["num_vehicles"]}\nDepot Index: {data["depot"]}")

    solution = solveTransportProblem(data_model=data)
    #solution = solveTransportProblemExample(data=data)

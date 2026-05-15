import numpy as np

from src.data_generator import generateDistanceMatrix, formatDataForVRPSolver
from src.london_locations import generateCustomerCoords
from src.solve_routing_problem import solveTransportProblem
from src.visualise_route import visualiseRoute

if __name__ == "__main__":
    RANDOM_SEED = 42
    np.random.seed(RANDOM_SEED)

    CHARING_CROSS_DEPOT = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }
    customers = generateCustomerCoords(customer_number=50)
    distance_matrix = generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)

    data_model = formatDataForVRPSolver(
        distance_matrix = distance_matrix,
        customer_demands = [0] + [1 for _ in customers],
        vehicle_capacities = [1 for _ in range(5)],
        vehicle_number = 4
    )

    solution_routes = solveTransportProblem(data_model=data_model)

    visualiseRoute(depot=CHARING_CROSS_DEPOT, customers=customers, routes=solution_routes, distance_matrix=distance_matrix)
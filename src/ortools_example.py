"""Simple Vehicles Routing Problem (VRP).

This is a sample using the routing library python wrapper to solve a VRP
problem.
A description of the problem can be found here:
http://en.wikipedia.org/wiki/Vehicle_routing_problem.

Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from src.london_locations import generateCustomerCoords
from src.data_generator import formatDataForVRPSolver, generateDistanceMatrix
import numpy as np


def getIntDistanceMatrix():
    return [
        [0, 16, 11, 8, 11, 20, 12, 10, 14, 19, 14],
        [16, 0, 9, 25, 22, 21, 27, 18, 31, 20, 7],
        [11, 9, 0, 19, 21, 25, 23, 9, 25, 24, 13],
        [8, 25, 19, 0, 12, 25, 7, 14, 6, 23, 22],
        [11, 22, 21, 12, 0, 12, 8, 22, 16, 11, 16],
        [20, 21, 25, 25, 12, 0, 21, 30, 29, 1, 14],
        [12, 27, 23, 7, 8, 21, 0, 21, 8, 20, 23],
        [10, 18, 9, 14, 22, 30, 21, 0, 19, 29, 20],
        [14, 31, 25, 6, 16, 29, 8, 19, 0, 28, 28],
        [19, 20, 24, 23, 11, 1, 20, 29, 28, 0, 12],
        [14, 7, 13, 22, 16, 14, 23, 20, 28, 12, 0]
    ]

def getNPDistanceMatrix():
    return [
        [0.0, 16.448150710292744, 11.352012250640238, 8.775027566905107, 11.450821845458504, 20.434521407720553, 12.375994770295337, 10.871418122570487, 14.904787617635964, 19.07800339842993, 14.26738983175181],
        [16.448150710292744, 0.0, 9.092804890477062, 25.21455740557747, 22.356132371268675, 21.846468724526336, 27.766070263629434, 18.163815691251248, 31.336893776076344, 20.615365763988827, 7.666535152768819],
        [11.352012250640238, 9.092804890477062, 0.0, 19.20412846539543, 21.22276038572414, 25.620249877605342, 23.727762156447778, 9.146277723573458, 25.019316555684057, 24.21765970941767, 13.00922635660163],
        [8.775027566905107, 25.21455740557747, 19.20412846539543, 0.0, 12.903196337186166, 25.01136478276139, 7.170141286700039, 14.703333870509763, 6.1306570953433415, 23.872499016215816, 22.54326040925278],
        [11.450821845458504, 22.356132371268675, 21.22276038572414, 12.903196337186166, 0.0, 12.566058631354288, 8.85764522597406, 22.295258940644533, 16.900553944690323, 11.63877140376627, 16.219425190426765],
        [20.434521407720553, 21.846468724526336, 25.620249877605342, 25.01136478276139, 12.566058631354288, 0.0, 21.33845792111928, 30.479251549465577, 29.451961315122382, 1.4204544808000628, 14.191667048314127],
        [12.375994770295337, 27.766070263629434, 23.727762156447778, 7.170141286700039, 8.85764522597406, 21.33845792111928, 0.0, 21.157789627572654, 8.58067836336635, 20.47503565234293, 23.18182031258466],
        [10.871418122570487, 18.163815691251248, 9.146277723573458, 14.703333870509763, 22.295258940644533, 30.479251549465577, 21.157789627572654, 0.0, 19.31458618977568, 29.07021110100073, 20.472705670715634],
        [14.904787617635964, 31.336893776076344, 25.019316555684057, 6.1306570953433415, 16.900553944690323, 29.451961315122382, 8.58067836336635, 19.31458618977568, 0.0, 28.458939371368732, 28.530241801290185],
        [19.07800339842993, 20.615365763988827, 24.21765970941767, 23.872499016215816, 11.63877140376627, 1.4204544808000628, 20.47503565234293, 29.07021110100073, 28.458939371368732, 0.0, 12.94959557394157],
        [14.26738983175181, 7.666535152768819, 13.00922635660163, 22.54326040925278, 16.219425190426765, 14.191667048314127, 23.18182031258466, 20.472705670715634, 28.530241801290185, 12.94959557394157, 0.0]
    ]


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    # data["distance_matrix"] = getIntDistanceMatrix()
    #     # fmt: off
    #     # fmt: on
    data["num_vehicles"] = 4
    data["depot"] = 0
    customers = generateCustomerCoords()
    CHARING_CROSS_DEPOT = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }
    distance_matrix = generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)
    data["distance_matrix"] = [[int(value) for value in row] for row in distance_matrix]
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()}")
    max_route_distance = 0
    for vehicle_id in range(data["num_vehicles"]):
        if not routing.IsVehicleUsed(solution, vehicle_id):
            continue
        index = routing.Start(vehicle_id)
        plan_output = f"Route for vehicle {vehicle_id}:\n"
        route_distance = 0
        while not routing.IsEnd(index):
            plan_output += f" {manager.IndexToNode(index)} -> "
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        plan_output += f"{manager.IndexToNode(index)}\n"
        plan_output += f"Distance of the route: {route_distance}m\n"
        print(plan_output)
        max_route_distance = max(route_distance, max_route_distance)
    print(f"Maximum of the route distances: {max_route_distance}m")



def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

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

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("No solution found !")


if __name__ == "__main__":
    np.random.seed(42)
    main()


def getDistanceMatrix():
    return [[np.float64(0.0), np.float64(12.824998578696926), np.float64(9.904464513854725), np.float64(14.622996598091344), np.float64(15.993872214588984), np.float64(25.435081071892007), np.float64(20.3737115801821), np.float64(22.595689927076307), np.float64(25.461822712347914), np.float64(20.426189577064537), np.float64(15.388820142325594)], [np.float64(12.824998578696926), np.float64(0.0), np.float64(20.589814076814747), np.float64(1.8762307818480584), np.float64(26.91379700796461), np.float64(28.287694259422953), np.float64(25.741233225331438), np.float64(33.60766191487083), np.float64(36.601434381052215), np.float64(18.71760371272986), np.float64(23.521851932892325)], [np.float64(9.904464513854725), np.float64(20.589814076814747), np.float64(0.0), np.float64(22.068426685024185), np.float64(6.362439989975317), np.float64(33.75871172177348), np.float64(12.833319295451727), np.float64(13.083593854286383), np.float64(16.054961412878463), np.float64(18.665830443158963), np.float64(21.855476141360636)], [np.float64(14.622996598091344), np.float64(1.8762307818480584), np.float64(22.068426685024185), np.float64(0.0), np.float64(28.3509452114143), np.float64(29.615756894416933), np.float64(26.467061513777317), np.float64(35.015468708585324), np.float64(38.015764753139024), np.float64(18.614158199949205), np.float64(25.299434793923783)], [np.float64(15.993872214588984), np.float64(26.91379700796461), np.float64(6.362439989975317), np.float64(28.3509452114143), np.float64(0.0), np.float64(38.19971142724046), np.float64(12.735893534425802), np.float64(6.721189440878258), np.float64(9.696591849180418), np.float64(22.21150941570714), np.float64(25.634142848786066)], [np.float64(25.435081071892007), np.float64(28.287694259422953), np.float64(33.75871172177348), np.float64(29.615756894416933), np.float64(38.19971142724046), np.float64(0.0), np.float64(45.694193743459515), np.float64(43.432094139112365), np.float64(45.590378928956305), np.float64(44.591725187716946), np.float64(12.906445060390839)], [np.float64(20.3737115801821), np.float64(25.741233225331438), np.float64(12.833319295451727), np.float64(26.467061513777317), np.float64(12.735893534425802), np.float64(45.694193743459515), np.float64(0.0), np.float64(15.707701844457503), np.float64(18.030866643778783), np.float64(12.387162880195941), np.float64(34.42229967812704)], [np.float64(22.595689927076307), np.float64(33.60766191487083), np.float64(13.083593854286383), np.float64(35.015468708585324), np.float64(6.721189440878258), np.float64(43.432094139112365), np.float64(15.707701844457503), np.float64(0.0), np.float64(3.0034166307581973), np.float64(27.0803484682952), np.float64(30.590800653123765)], [np.float64(25.461822712347914), np.float64(36.601434381052215), np.float64(16.054961412878463), np.float64(38.015764753139024), np.float64(9.696591849180418), np.float64(45.590378928956305), np.float64(18.030866643778783), np.float64(3.0034166307581973), np.float64(0.0), np.float64(29.742575493125624), np.float64(32.69649728502733)], [np.float64(20.426189577064537), np.float64(18.71760371272986), np.float64(18.665830443158963), np.float64(18.614158199949205), np.float64(22.21150941570714), np.float64(44.591725187716946), np.float64(12.387162880195941), np.float64(27.0803484682952), np.float64(29.742575493125624), np.float64(0.0), np.float64(35.79807620411878)], [np.float64(15.388820142325594), np.float64(23.521851932892325), np.float64(21.855476141360636), np.float64(25.299434793923783), np.float64(25.634142848786066), np.float64(12.906445060390839), np.float64(34.42229967812704), np.float64(30.590800653123765), np.float64(32.69649728502733), np.float64(35.79807620411878), np.float64(0.0)]]
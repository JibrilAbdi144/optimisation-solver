import numpy as np
import matplotlib.pyplot as plt

def generateCustomers(customer_number: int, x_range: tuple[float, float], y_range: tuple[float, float]) -> list[dict[str, float]]:

    customers = []
    for index in range(customer_number):
        customer_xposition = np.random.uniform(low=x_range[0], high=x_range[1])
        customer_yposition = np.random.uniform(low=y_range[0], high=y_range[1])
        customer_demand = 1.0 + 5 * np.random.normal() ** 2

        customers.append({
            "xposition": customer_xposition,
            "yposition": customer_yposition,
            "demand": customer_demand
        })

    return customers

def calculate2DEuclideanDistance(point1, point2) -> float:
    return float(np.sqrt((point1["xposition"] - point2["xposition"]) ** 2 + (point1["yposition"] - point2["yposition"]) ** 2))

def calculateHaversineDistance(point1, point2) -> float:
    delta_latitude = np.radians(point1["latitude"] - point2["latitude"])
    delta_longitude = np.radians(point1["longitude"] - point2["longitude"])


    a = (np.sin(delta_latitude / 2)) ** 2 + np.cos(np.radians(point1["latitude"])) * np.cos(np.radians(point2["latitude"])) * np.sin(delta_longitude / 2) ** 2
    c = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))

    EARTH_RADIUS = 6371000
    distance = EARTH_RADIUS * c
    return int(distance)

def generateDistanceMatrix(depot: dict[str, float], customers: list[dict[str, float]]) -> list[list[float]]:
    points = [depot] + customers
    matrix_size = len(points)
    distance_matrix = [[0. for _ in range(matrix_size)] for _ in range(matrix_size)]

    for i, point1 in enumerate(points):
        for j, point2 in enumerate(points):
            #euclidean_distance = calculate2DEuclideanDistance(point1=point1, point2=point2)
            distance = calculateHaversineDistance(point1=point1, point2=point2)
            distance_matrix[i][j] = distance
    
    return distance_matrix

def printDistanceMatrix(distance_matrix: list[list], precision_level: int=0) -> None:
    column_width = 15

    header_output = ""
    header_output += "|" + " " * column_width
    for index, _ in enumerate(distance_matrix):
        if index == 0:
            text = "Depot"
        else:
            text = f"Customer {index}"
        header_output += ("|" + f"{text:^{column_width}}")
    header_output += "|"

    divider_output = ""
    divider_output += "|" + "-" * column_width
    for index, _ in enumerate(distance_matrix):
        divider_output += ("|" + "-" * column_width)
    divider_output += "|"

    print(header_output)
    print(divider_output)

    for i, row in enumerate(distance_matrix):
        body_output = ""
        if i == 0:
            text = "Depot"
        else:
            text = f"Customer {i}"
        body_output += ("|" + f"{text:^{column_width}}")
        for j, item in enumerate(row):
            body_output += ("|" + f"{item:^{column_width}.{precision_level}f}")
        body_output += "|"
        print(body_output)

def formatDataForVRPSolver(distance_matrix: list[list], customer_demands: list, vehicle_capacities: list[int]=[15, 15], vehicle_number: int=2) -> dict:
    number_of_vehicles = 4
    data = {}
    data["distance_matrix"] = distance_matrix
    data["demands"] = customer_demands
    data["vehicle_capacities"] = vehicle_capacities
    data["num_vehicles"] = vehicle_number
    data["depot"] = 0

    return data
        
        

# if __name__ == "__main__":
#     SEED_VALUE = 42
#     np.random.seed(SEED_VALUE)

#     depot = {"xposition":0., "yposition":0.}
#     customer_number = 10
#     customers = generateCustomers(customer_number=customer_number, x_range=(-100,100), y_range=(-100, 100))
#     distance_matrix = generateDistanceMatrix(depot=depot, customers=customers)

#     printDistanceMatrix(distance_matrix=distance_matrix, precision_level=2)
#     #print("\n")
#     # for index, customer in enumerate(customers):
#     #     print(f"Customer {index + 1}: Demand: {customer["demand"]:.1f}")

#     vehicle_capacities = [15 for i in range(2)]
#     vehicle_number = 2

#     data = formatDataForVRPSolver(distance_matrix=distance_matrix, customer_demands=[customer["demand"] for customer in customers], vehicle_capacities=vehicle_capacities, vehicle_number=vehicle_number)

#     figure, axes = plt.subplots()
#     axes.scatter(
#         x=[depot["xposition"]] + [customer["xposition"] for customer in customers],
#         y=[depot["yposition"]] + [customer["yposition"] for customer in customers],
#         color = ["red"] + ["blue" for customer in customers]
#     )
#     plt.show()

    #print(data)

if __name__ == "__main__":
    depot = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }
    customer = {
        "latitude": 51.529285062031455,
        "longitude":0.10771375902808533
    }
    distance = calculateHaversineDistance(
        point1=depot,
        point2=customer
    )
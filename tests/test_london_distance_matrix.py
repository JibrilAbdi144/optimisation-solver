from src.london_locations import generateCustomerCoords
from src.data_generator import generateDistanceMatrix, printDistanceMatrix, calculateHaversineDistance
import numpy as np

if __name__ == "__main__":
    SEED_VALUE = 42
    np.random.seed(SEED_VALUE)
    customers = generateCustomerCoords()
    #CHARING CROSS 51.50708506805912, -0.12730860068255712
    depot = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }

    print(f"Latitude: {customers[0]["latitude"]}\nLongitude: {customers[0]["longitude"]}")

    print(f"Distance between Depot and Customer 1: {calculateHaversineDistance(depot, customers[0])}")    

    distance_matrix = generateDistanceMatrix(depot=depot, customers=customers)
    
    printDistanceMatrix(distance_matrix=distance_matrix, precision_level=3)
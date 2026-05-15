import streamlit as st
from streamlit_folium import st_folium
import numpy as np

from src.data_generator import generateDistanceMatrix, formatDataForVRPSolver
from src.london_locations import generateCustomerCoords
from src.solve_routing_problem import solveTransportProblem
from src.visualise_route import visualiseRoute, getRouteCost

CHARING_CROSS_DEPOT = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }

def buttonClick(customer_number, vehicle_number, vehicle_capacity):
    customers = generateCustomerCoords(customer_number=customer_number)
    distance_matrix = generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)

    data_model = formatDataForVRPSolver(
        distance_matrix=distance_matrix,
        customer_demands=[0] + [1 for _ in customers],
        vehicle_capacities=[vehicle_capacity for _ in range(vehicle_number)],
        vehicle_number=vehicle_number
    )

    solution_routes = solveTransportProblem(data_model=data_model)
    visualiseRoute(depot=CHARING_CROSS_DEPOT, customers=customers, routes=solution_routes, distance_matrix=distance_matrix)


if __name__ == "__main__":

    SEED_VALUE = 42
    np.random.seed(SEED_VALUE)

    st.title("Route Optimisation Solver", text_alignment="center")

    with st.sidebar:
        st.header("User inputs", text_alignment="center")
        customer_number = st.number_input("Number of Customers", min_value=5, max_value=50)
        vehicle_number = st.number_input("Vehicle Number", min_value = 1, max_value=10)
        vehicle_capacity = st.number_input("Vehicle Capacity", min_value = 5, max_value=20)
        optimise_button = st.button(
            label="Optimise!",
            type="primary",
            use_container_width=True,
            on_click=lambda: buttonClick(
                customer_number=customer_number,
                vehicle_capacity=vehicle_capacity,
                vehicle_number=vehicle_number
            )
        )

    with open("london_map.html", "r", encoding="utf-8") as map_file:
        html_data = map_file.read()

    st.iframe(html_data, height=500)

import streamlit as st
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt

from src.data_generator import generateDistanceMatrix, formatDataForVRPSolver
from src.london_locations import generateCustomerCoords
from src.solve_routing_problem import solveTransportProblem
from src.visualise_route import visualiseRoute, getRouteCost

if "results" not in st.session_state:
    st.session_state["results"] = None

CHARING_CROSS_DEPOT = {
        "latitude": 51.50708506805912,
        "longitude": -0.12730860068255712
    }

def buttonClick(customer_number, customer_demand, vehicle_number, vehicle_capacity):
    customers = generateCustomerCoords(customer_number=customer_number)
    distance_matrix = generateDistanceMatrix(depot=CHARING_CROSS_DEPOT, customers=customers)

    data_model = formatDataForVRPSolver(
        distance_matrix=distance_matrix,
        customer_demands=[0] + [customer_demand for customer in customers],
        vehicle_capacities=[vehicle_capacity for _ in range(vehicle_number)],
        vehicle_number=vehicle_number
    )

    solution_routes = solveTransportProblem(data_model=data_model)
    visualiseRoute(depot=CHARING_CROSS_DEPOT, customers=customers, routes=solution_routes, distance_matrix=distance_matrix)
    st.session_state["results"] = {
        "solution_routes": solution_routes,
        "distance_matrix": distance_matrix
    }


if __name__ == "__main__":

    SEED_VALUE = 42
    np.random.seed(SEED_VALUE)

    st.title("Route Optimisation Solver", text_alignment="center")

    with st.sidebar:
        st.header("User inputs", text_alignment="center")
        customer_number = st.number_input("Number of Customers", value=5, min_value=1, max_value=50)
        customer_demand = st.number_input("Customer Demand", value=1, min_value=1, max_value=10)
        vehicle_number = st.number_input("Vehicle Number", value=4,  min_value = 1, max_value=10)
        vehicle_capacity = st.number_input("Vehicle Capacity", value=10,  min_value = 5, max_value=20)

        if customer_number * customer_demand > vehicle_number * vehicle_capacity:
            st.warning("Warning: Customer demand exceeds vehicle capacity")
            warning = True
        else:
            warning = False

        optimise_button = st.button(
            label="Optimise!",
            type="primary",
            use_container_width=True,
            on_click=lambda: buttonClick(
                customer_number=customer_number,
                customer_demand = customer_demand,
                vehicle_capacity=vehicle_capacity,
                vehicle_number=vehicle_number,
            ),
            disabled=warning
        )

        

    with open("london_map.html", "r", encoding="utf-8") as map_file:
        html_data = map_file.read()

    st.iframe(html_data, height=500)

    if st.session_state.get("results"):

        results = st.session_state["results"]
        route_costs = [getRouteCost(route=route, distance_matrix=results["distance_matrix"]) / 1000 for route in results["solution_routes"]]

        st.subheader("Key Metrics")
        columns = st.columns(spec=3)
        columns[0].metric(label="Total Distance", value=f"{sum(route_costs):.1f} km")
        columns[1].metric(label="Max Distance", value=f"{max(route_costs):.1f} km")
        columns[2].metric(label="Min Distance", value=f"{min(route_costs):.1f} km")

        figure, axes = plt.subplots()
        axes.bar(x=[f"Route {i}" for i in range(len(route_costs))], height=route_costs)
        axes.set_xlabel("Vehicle Routes")
        axes.set_ylabel("Route Distance (km)")
        axes.set_title("Vehicle Route Distances")
        st.pyplot(figure)
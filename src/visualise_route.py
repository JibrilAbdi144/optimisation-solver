import folium

def visualiseRoute(depot, customers, routes, distance_matrix):

    london_map = folium.Map(location=[depot["latitude"], depot["longitude"]], zoom_start=10)

    points = [depot] + customers
    route_colours = ["red", "green", "yellow", "blue"]
    for route_number, route in enumerate(routes):
        for index in range(len(route) - 1):
            from_point = points[route[index]]
            to_point = points[route[index + 1]]

            folium.PolyLine(
                locations=[
                    [from_point["latitude"], from_point["longitude"]],
                    [to_point["latitude"], to_point["longitude"]]
                ],
                popup=f"Route {route_number} Cost: {getRouteCost(route=route, distance_matrix=distance_matrix)}",
                color=route_colours[route_number % len(route_colours)],
                weight=2
            ).add_to(london_map)

    folium.Marker(
        location=[depot["latitude"], depot["longitude"]],
        popup="Depot (Charing Cross)"
    ).add_to(london_map)
    for index, customer in enumerate(customers):
        folium.Marker(
            location=[customer["latitude"], customer["longitude"]],
            popup=f"Customer {index + 1}"
        ).add_to(london_map)

    london_map.save("london_map.html")


def getRouteCost(route, distance_matrix):
    cost = 0
    for index in range(len(route) - 1):
        from_node = route[index]
        to_node = route[index + 1]
        cost += distance_matrix[from_node][to_node]
    return cost
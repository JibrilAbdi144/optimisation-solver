import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import Point
import numpy as np
import folium
import webbrowser


def getLondonBoundary():
    #return gpd.read_file(r"C:\Users\jibri\OneDrive\Documents\Maths Projects\optimisation-solver\gla\gla\London_GLA_Boundary.shp").to_crs("EPSG:4326")
    return gpd.read_file("gla/gla/London_GLA_Boundary.shp").to_crs("EPSG:4326")

def generateCustomerCoords(customer_number: int=10) -> list[dict[str, float | float]]:
    '''
    Randomly generates the latitude-longitude coordinates of customers within the Greater London boundary.

    Arguments:
        london_boundary (gpd.GeoDataFrame): Boundary of the Greater London Area.
        customer_number (int, optional): Number of customers.
    
    Returns:
        points (list[Point]): List of customer coordinates.
    '''
    points = []
    london_boundary = getLondonBoundary()
    minlong, minlat, maxlong, maxlat = london_boundary.total_bounds
    while len(points) < customer_number:
        point_x = np.random.uniform(minlong, maxlong)
        point_y = np.random.uniform(minlat, maxlat)
        point = Point(point_x, point_y)
        if point.within(london_boundary.geometry.union_all()):
            points.append(point)
    return [{
        "latitude": point.y,
        "longitude": point.x
    } for point in points]



if __name__ == "__main__":
    SEED_VALUE = 42
    np.random.seed(SEED_VALUE)

    #london_boundary = gpd.read_file(r"C:\Users\jibri\OneDrive\Documents\Maths Projects\optimisation-solver\gla\gla\London_GLA_Boundary.shp").to_crs("EPSG:4326")

    #london_boundary = gpd.read_file(r"..\gla\gla\London_GLA_Boundary.shp").to_crs("EPSG:4326")
    #print("Hello world")

    # london_bounding_box = london_boundary.geometry.union_all()
    # minx, miny, maxx, maxy = london_boundary.total_bounds

    # if london_boundary.crs is not None:
    #     print(london_boundary.crs.axis_info)

    # points = []
    # points_number = 16
    # while len(points) < points_number:
    #     point = Point(np.random.uniform(minx, maxx), np.random.uniform(miny, maxy))
    #     #print(type(point), type(london_boundary))
    #     if point.within(london_boundary.geometry.union_all()):
    #         points.append(point)

    points = generateCustomerCoords()

    # figure, axes = plt.subplots()
    # london_boundary.plot(ax=axes, facecolor="none", edgecolor="black")
    # london_rectangle = patches.Rectangle((minx, miny), maxx - minx, maxy - miny, facecolor="none", edgecolor="black")
    # axes.add_patch(london_rectangle)
    # axes.scatter([point.x for point in points], [point.y for point in points])
    # plt.show()

    #gdf_points = gpd.GeoDataFrame(geometry=points, crs="EPSG:27700").to_crs(crs="EPSG:4326")

    london_map = folium.Map(location=[51.5, -0.1], zoom_start=10)


    for point in points:
        folium.Marker(location=[point["latitude"], point["longitude"]], ).add_to(london_map)
    
    #folium.GeoJson(london_boundary.geometry).add_to(london_map)
    #folium.Rectangle([(miny, minx), (maxy, maxx)]).add_to(london_map)


    london_map.save("london_map.html")
    #webbrowser.open("london_map.html")
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay


def select_equidistant_points(contour, num_points):
    # Ta funkcja pozostaje bez zmian
    contour = contour.squeeze()
    n = len(contour)
    step = n // num_points

    selected_points = contour[::step]
    return selected_points


def calculate_average_distance(contour):
    # Obliczanie średniej odległości między sąsiednimi punktami konturu
    distances = []
    for i in range(len(contour)):
        next_index = (i + 1) % len(contour)
        distance = np.linalg.norm(contour[i] - contour[next_index])  # linalg liczy odlegosc miedzy puntkami
        distances.append(distance)
    return np.mean(distances)   # to je średnia


def create_equidistant_grid_inside_contour(contour, distance):
    # Znajdowanie granic obszaru konturu - Zwraca ona krotkę lewego górnego rogu oraz szerokość i wysokość konturu
    x_min, y_min, w, h = cv2.boundingRect(contour)

    # Obliczenie wysokości trójkąta równobocznego na podstawie długości boku
    triangle_height = (np.sqrt(3) / 2) * distance

    # Inicjalizacja listy punktów
    points = []

    # Generowanie siatki punktów
    y = y_min
    row = 0
    while y < y_min + h:
        x_offset = (triangle_height if row % 2 == 1 else 0)
        x = x_min + x_offset
        while x < x_min + w:
            if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                points.append((x, y))
            x += distance
        y += triangle_height
        row += 1

    return np.array(points)


# Wczytanie obrazu i przekształcenia
image = cv2.imread('atomowka.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 30, 200)
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Select equidistant points from the contour
num_points = 30  # ilosc punktow we froncie
selected_points = select_equidistant_points(contours[0], num_points)

# Obliczanie średniej odległości między punktami na konturze
average_distance = calculate_average_distance(selected_points)

# Generowanie siatki punktów wewnątrz konturu z wykorzystaniem obliczonej odległości
grid_points = create_equidistant_grid_inside_contour(contours[0], average_distance)


def display_points(selected_points, grid_points, all_points, contour):
    # Wizualizacja
    tri = Delaunay(all_points)

    # Rysowanie siatki za pomocą triangulacji Delaunay
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Rysowanie punktów
    ax.scatter(selected_points[:, 0], selected_points[:, 1], c='r')  # czerwone - punkty na konturze
    ax.scatter(grid_points[:, 0], grid_points[:, 1], c='indigo')  # indigo - punkty wewnątrz konturu

    # Rysowanie linii tworzących siatkę tylko wewnątrz konturu
    for simplex in tri.simplices:
        triangle = all_points[simplex]
        centroid = np.mean(triangle, axis=0)
        if cv2.pointPolygonTest(contour, (int(centroid[0]), int(centroid[1])), False) >= 0:
            for i in range(3):
                start, end = simplex[i], simplex[(i + 1) % 3]
                pt1, pt2 = all_points[start], all_points[end]
                ax.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color='blue')

    plt.show()


def combine_points(selected_points, grid_points):
    all_points = np.vstack([selected_points, grid_points])
    return all_points


# Kombinowanie punktów z frontu i ze środka
all_points = combine_points(selected_points, grid_points)

# Wywołanie funkcji display_points z wszystkimi punktami
display_points(selected_points, grid_points, all_points, contours[0])

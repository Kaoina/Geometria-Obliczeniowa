import cv2
# import numpy as np
import matplotlib.pyplot as plt


def select_equidistant_points(contour, num_points):
    contour = contour.squeeze()
    n = len(contour)
    step = n // num_points
    # to jest wybieranie co step wyliczony
    selected_points = contour[::step]
    return selected_points


# Wczytanie obrazu
image = cv2.imread('pacman_duch.png')
# image = cv2.imread('trudny_wariant.png')
# image = cv2.imread('atomowka.png')

# Grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Find Canny edges
edged = cv2.Canny(gray, 30, 200)

# Znajdowanie konturów - opcja external - tylko zewnetrzny kontur
contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Select equidistant points from the contour
num_points = 20  # ilosc punktow we froncie
selected_points = select_equidistant_points(contours[0], num_points)

# # Wizualizacja figury, frontu
# Rysowanie figury
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# Rysowanie punktów (: to wszystkie wiersze z danej tablicy, liczba oznacza kolumnę)
plt.scatter(selected_points[:, 0], selected_points[:, 1], c='Maroon')

# Pokazanie wykresu
plt.show()

plt.show()

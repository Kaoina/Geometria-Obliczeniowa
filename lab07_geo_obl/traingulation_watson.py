import math
import numpy as np
import matplotlib.pyplot as plt
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):  # dostęp do współrzędnych punktu za pomocą indeksu
        if index == 0:
            return self.x
        else:
            return self.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)   # porównoje ktory "mniejszy"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)   # sprawdzanie czy rowne

    def __hash__(self):
        return hash((self.x, self.y))


class Triangle:
    def __init__(self, vertices):
        self.vertices = np.array([(v.x, v.y) for v in vertices])
        self.edges = [tuple(sorted([vertices[i], vertices[(i + 1) % 3]])) for i in range(3)]  # trzy wierchołki w trzech krotkach
        self.circumcenter, self.radius = self.find_circumcenter_and_radius()   # środek i promień
        self.edge_lengths = self.calculate_edge_lengths()  # lista długości boków trójkątów

    def find_circumcenter_and_radius(self):
        ax, ay = self.vertices[0]
        bx, by = self.vertices[1]
        cx, cy = self.vertices[2]
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        # współrzędna x i y środka okręgu opisanego jakies magiczne wzory
        ux = ((ax ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
        uy = ((ax ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax - cx) + (cx ** 2 + cy ** 2) * (bx - ax)) / d
        radius = np.sqrt((ux - ax) ** 2 + (uy - ay) ** 2)
        return (ux, uy), radius

    def calculate_edge_lengths(self):
        lengths = []
        for i in range(3):
            j = (i + 1) % 3
            lengths.append(np.linalg.norm(self.vertices[i] - self.vertices[j]))   # liczy długosc wektorw
        return lengths

    def quality_ratio(self):
        min_length = min(self.edge_lengths)
        max_length = max(self.edge_lengths)
        return min_length / max_length if max_length > 0 else 0

    def circumcircle_contains(self, point):
        # Oblicz odległość od środka okręgu opisanego do punktu
        distance = math.sqrt((point.x - self.circumcenter[0]) ** 2 + (point.y - self.circumcenter[1]) ** 2)
        return distance <= self.radius


def analyze_triangulation_quality(triangulation):
    quality_ratios = [triangle.quality_ratio() for triangle in triangulation]
    plt.hist(quality_ratios, bins=20, edgecolor='black', color='magenta')
    plt.xlabel('Stosunek najkrótszego boku do najdłuższego')
    plt.ylabel('Liczba trójkątów')
    plt.title('Histogram jakości trójkątów')
    plt.show()
    return np.mean(quality_ratios), np.median(quality_ratios), min(quality_ratios), max(quality_ratios)


def create_super_triangle(points):
    # Oblicz środek ciężkości punktów
    avg_x = sum(p.x for p in points) / len(points)
    avg_y = sum(p.y for p in points) / len(points)

    max_distance = max(math.sqrt((p.x - avg_x) ** 2 + (p.y - avg_y) ** 2) for p in points)

    d = max_distance * 3

    return Triangle([
        Point(avg_x - d, avg_y - d),
        Point(avg_x, avg_y + d),
        Point(avg_x + d, avg_y - d)
    ])


def bowyer_watson(points):
    super_triangle = create_super_triangle(points)
    triangulation = [super_triangle]

    for point in points:
        bad_triangles = [t for t in triangulation if t.circumcircle_contains(point)]
        edges = set()
        for t in bad_triangles:
            for edge in t.edges:
                if edge in edges:
                    edges.remove(edge)
                else:
                    edges.add(edge)

        triangulation = [t for t in triangulation if t not in bad_triangles]
        for edge in edges:
            triangulation.append(Triangle([edge[0], edge[1], point]))

    # Remove triangles containing vertices of the super triangle
    triangulation = [t for t in triangulation if not any(
        np.array_equal(vertex, super_triangle.vertices[i]) for vertex in t.vertices for i in range(3))]

    return triangulation


def load_points_from_file(filename):
    with open(filename, 'r') as file:
        num_points = int(file.readline().strip())
        points = []
        for _ in range(num_points):
            x, y = map(float, file.readline().split())
            points.append(Point(x, y))
    return points


def visualize_triangulation(triangulation, points, super_triangle):
    for tri in triangulation:
        vertices = tri.vertices
        plt.triplot(vertices[:, 0], vertices[:, 1], color='maroon')

    plt.plot([p.x for p in points], [p.y for p in points], 'o', color='black')

    # Wyświetlenie super trójkąta
    # super_vertices = super_triangle.vertices
    # xs = [v[0] for v in super_vertices] + [super_vertices[0][0]]
    # ys = [v[1] for v in super_vertices] + [super_vertices[0][1]]
    # plt.plot(xs, ys, color='gold')

    plt.title('Bowyer-Watson Triangulation')
    plt.grid(True)
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def main():
    filename = "punkty_delunaj.txt"
    #filename = "punkty_delunay_wiecej.txt"
    my_points = load_points_from_file(filename)

    # Triangulacja Delaunay'a (Bowyer-Watson)
    start_time = time.time()
    super_triangle = create_super_triangle(my_points)
    delaunay_triangulation = bowyer_watson(my_points)
    delaunay_time = time.time() - start_time

    # Analiza triangulacji Delaunay'a
    delaunay_num_elements = len(delaunay_triangulation)

    # Analiza jakości trójkątów
    mean_quality, median_quality, min_quality, max_quality = analyze_triangulation_quality(delaunay_triangulation)

    # Wyświetlenie wyników
    print("Triangulacja Delaunay'a (Bowyer-Watson):")
    print(f"Liczba elementów: {delaunay_num_elements}")
    print(f"Średnia jakość trójkątów: {mean_quality:.4f}")
    print(f"Mediana jakości trójkątów: {median_quality:.4f}")
    print(f"Najniższa jakość trójkąta: {min_quality:.4f}")
    print(f"Najwyższa jakość trójkąta: {max_quality:.4f}")
    print(f"Czas wykonania: {delaunay_time:.4f} s")

    # Wizualizacja triangulacji Bowyer-Watson
    # visualize_triangulation(delaunay_triangulation, my_points)
    visualize_triangulation(delaunay_triangulation, my_points, super_triangle)


if __name__ == "__main__":
    main()

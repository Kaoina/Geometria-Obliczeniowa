import matplotlib.pyplot as plt
import math

hull = []


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def read_points(filename):
    with open(filename, 'r') as file:
        num_points = int(file.readline())
        points = []
        for line in file:
            x, y = map(int, line.strip().split())
            points.append(Point(x, y))
    return points, num_points


def show_points(points):
    # Extract x and y coordinates from the points
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]

    # Create the scatter plot
    plt.scatter(x_coords, y_coords, color='red', marker='*')
    plt.title("Zbiór punktów z pliku")
    plt.axis("equal")
    plt.show()


def show_jarvis(points, name):
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    hull_list_x, hull_list_y = jarvis(points)

    plt.scatter(x_coords, y_coords, color='gold', marker='*')
    leng = len(hull_list_x)
    for i in range(leng):
        if i == leng - 1:
            j = 0  # Connect the last element to the first element
        else:
            j = i + 1
        plt.plot([hull_list_x[i], hull_list_x[j]], [hull_list_y[i], hull_list_y[j]], marker='x')

    plt.title("Otoczka wypukła jarvis dla pliku " + name)
    plt.axis("equal")
    plt.show()


def smallest_index(points):
    minn = 0
    for i in range(1, len(points)):
        if points[i].x < points[minn].x:
            minn = i
        elif points[i].x == points[minn].x:
            if points[i].y > points[minn].y:
                minn = i
    return minn


def highest_index(points):
    maxx = 0
    for i in range(1, len(points)):
        if points[i].x > points[maxx].x:
            maxx = i
        elif points[i].x == points[maxx].x:
            if points[i].y < points[maxx].y:
                maxx = i
    return maxx


def orientation(p, q, r):
    # iloczyn wektorowy dwóch wektorów
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    # punkty sa wspoliniowe -> sin0
    if val == 0:
        return 0
    # punkt r jest po lewej stronie odcinak pq
    elif val > 0:
        return 1
    # punkt r jest po prawej stronie odcinak pq
    else:
        return 2


def jarvis(points):
    quantity = len(points)
    if quantity < 3:
        return

    s = smallest_index(points)

    hull_jarvis = []
    p = s
    while True:
        hull_jarvis.append(p)
        # aby mozna bylo zatoczyc kolo
        q = (p + 1) % quantity

        for i in range(quantity):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        # koło się zatoczyło
        if p == s:
            break

    # for each in hull_jarvis:
    #     print(points[each].x, points[each].y)

    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    hull_x = [x_coords[i] for i in hull_jarvis]
    hull_y = [y_coords[i] for i in hull_jarvis]

    return hull_x, hull_y


def find_side(p1, p2, p):
    val = (p.y - p1.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p.x - p1.x)

    if val > 0:
        return 1
    if val < 0:
        return -1
    return 0


def line_dist(p1, p2, p):
    # odległość punktu od prostej z różnicy iloczynów skalarnych
    return abs((p.y - p1.y) * (p2.x - p1.x) - (p2.y - p1.y) * (p.x - p1.x))


def quick_hull(points, quantity, p1, p2, side):
    ind = -1
    max_dist = 0

    for i in range(quantity):
        temp = line_dist(p1, p2, points[i])
        if (find_side(p1, p2, points[i]) == side) and (temp > max_dist):
            ind = i
            max_dist = temp
    # jak if wyzej sie nie wykona no to nie ma kolejneogo punktu dalej oddalonego po dobrej stornie
    if ind == -1:
        hull.append(p1)
        hull.append(p2)
        return

    quick_hull(points, quantity, points[ind], p1, -find_side(points[ind], p1, p2))
    quick_hull(points, quantity, points[ind], p2, -find_side(points[ind], p2, p1))
    return hull


def print_hull(points, quantity):
    if quantity < 3:
        return

    min_x = smallest_index(points)
    max_x = highest_index(points)

    hull_up = quick_hull(points, quantity, points[min_x], points[max_x], 1)
    hull_down = quick_hull(points, quantity, points[min_x], points[max_x], -1)

    total_hull = []
    for each in hull_up:
        total_hull.append(each)
    for each in hull_down:
        total_hull.append(each)

    return total_hull


def sort_points_clockwise(points):
    # robi śrendia z wspolrzednych i znajduje środek naszych punktów
    center_x = sum(p.x for p in points) / len(points)
    center_y = sum(p.y for p in points) / len(points)

    # przesuwamy gdzie do ukladu gdzie srodek 0,0
    for p in points:
        p.x -= center_x
        p.y -= center_y

    # atan2 zwraca kąt w radianach między osią x a punktem z uwzględnieniem ćwiartki!!
    points.sort(key=lambda p: (math.atan2(p.y, p.x)))

    # wracamy do starych współrzędnych
    for p in points:
        p.x += center_x
        p.y += center_y

    return points


def show_quick(points, name, quantity):
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    total_hull = print_hull(points, quantity)

    unique = list(set(total_hull))
    filtered = sort_points_clockwise(unique)

    length = len(filtered)
    for i in range(length):
        plt.plot([filtered[i].x, filtered[(i + 1) % length].x], [filtered[i].y, filtered[(i + 1) % length].y])

    plt.scatter(x_coords, y_coords, color='gold', marker='*')
    plt.title("Otoczka wypukła quick hull dla pliku " + name)
    plt.axis("equal")
    plt.show()


my_file = "ksztalt_3.txt"
my_points, amount = read_points(my_file)
# show_points(my_points)
show_jarvis(my_points, my_file)
# show_quick(my_points, my_file, amount)

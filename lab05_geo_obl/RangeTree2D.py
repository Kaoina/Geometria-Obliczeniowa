import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TreeNode:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None


class RangeTree2D:
    def __init__(self, points):
        self.root = self.build(points, depth=0)

    def build(self, points, depth):
        if not points:
            return None

        axis = depth % 2
        points.sort(key=lambda point: getattr(point, 'x' if axis == 0 else 'y'))
        median = len(points) // 2

        root = TreeNode(points[median])
        root.left = self.build(points[:median], depth + 1)
        root.right = self.build(points[median + 1:], depth + 1)
        return root


def find_range(root, x_min, x_max, y_min, y_max):
    results = []

    def search(node, depth=0):
        if node is None:
            return

        axis = depth % 2
        coord = node.point.x if axis == 0 else node.point.y
        range_min = x_min if axis == 0 else y_min
        range_max = x_max if axis == 0 else y_max

        if x_min <= node.point.x <= x_max and y_min <= node.point.y <= y_max:
            results.append(node.point)

        if coord >= range_min:
            search(node.left, depth + 1)

        if coord <= range_max:
            search(node.right, depth + 1)

    search(root)
    return results


def read_points(filename):
    with open(filename, 'r') as file:
        num_points = int(file.readline())
        points = []
        for line in file:
            x, y = map(int, line.strip().split())
            points.append(Point(x, y))
    return points


def show_points(points, range_points):
    # Extract x and y coordinates from the points
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]

    x_coords_r = [point.x for point in range_points]
    y_coords_r = [point.y for point in range_points]

    # Create the scatter plot
    plt.scatter(x_coords, y_coords, color='red')
    plt.scatter(x_coords_r, y_coords_r, color='blue')
    plt.title("Points")
    plt.grid(True)
    plt.axis("equal")
    plt.show()


def print_2d_util(node, space):
    if node is None:
        return

    space += 10
    print_2d_util(node.right, space)

    print()
    for i in range(10, space):
        print(" ", end="")
    print(node.point.x, ",", node.point.y)

    print_2d_util(node.left, space)


def print_2d(root):
    print_2d_util(root, 0)


my_file = "lab05_dane_2D.txt"
my_points = read_points(my_file)

points_2d = read_points(my_file)
kd_tree = RangeTree2D(my_points)

print("KD tree: \n")
print_2d(kd_tree.root)

choose_x_min = -5
choose_x_max = 0
choose_y_min = -7.5
choose_y_max = 5
points_in_range = find_range(kd_tree.root, choose_x_min, choose_x_max, choose_y_min, choose_y_max)
print("Points between x: ", choose_x_min, "-", choose_x_max, "| y: ", choose_y_min, "-", choose_y_max, "  is: ")
for point in points_in_range:
    print(point.x, point.y)
show_points(my_points, points_in_range)

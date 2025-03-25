def read_points_from_file(file_name):
    points = []
    with open(file_name, 'r') as file:
        num_points = int(file.readline().strip())
        for _ in range(num_points):
            point = int(file.readline().strip())
            points.append(point)
    return points


class RangeTreeNode:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None


class RangeTree1D:
    def __init__(self, points):
        self.root = self.build(points)

    def build(self, points):
        if not points:
            return None

        median = len(points) // 2
        first_half = points[:median]
        second_half = points[median + 1:]

        root = RangeTreeNode(points[median])
        root.left = self.build(first_half)
        root.right = self.build(second_half)
        return root

    def search_range(self, min_val, max_val, node=None):
        if node is None:
            node = self.root

        result = []
        if min_val <= node.point <= max_val:
            result.append(node.point)

        if node.left and min_val < node.point:
            result.extend(self.search_range(min_val, max_val, node.left))
        if node.right and max_val > node.point:
            result.extend(self.search_range(min_val, max_val, node.right))

        return result


def print_1d_util(node, space):
    if node is None:
        return

    space += 10
    print_1d_util(node.right, space)

    print()
    for i in range(10, space):
        print(" ", end="")
    print(node.point)

    print_1d_util(node.left, space)


def print_1d(root):
    print_1d_util(root, 0)


my_file = "lab05_dane_1D.txt"
points_1d = read_points_from_file(my_file)
points_1d.sort()
print("My points: \n", points_1d)

range_tree_1d = RangeTree1D(points_1d)
print("1D range tree: \n")
print_1d(range_tree_1d.root)

min_range = -5
max_range = 17
points_in_range = range_tree_1d.search_range(min_range, max_range)

print("Points between ", min_range, " and ", max_range, " :", points_in_range)

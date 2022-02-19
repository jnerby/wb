import random
import collections
import operator
from math import hypot

random.seed(1)  # Setting random number generator seed for repeatability

NUM_DRONES = 10000
AIRSPACE_SIZE = 128000 # 128 km
CONFLICT_RADIUS = 500  # Meters.

# def count_conflicts(drones, conflict_radius):
#     raise Exception("You must implement this function")

def gen_coord():
    return int(random.random() * AIRSPACE_SIZE)

# positions = [[gen_coord(), gen_coord()] for i in range(NUM_DRONES)]
# conflicts = count_conflicts(positions, CONFLICT_RADIUS)
# print("Drones in conflict: {}".format(conflicts))


BinaryTree = collections.namedtuple("BinaryTree", ["value", "left", "right"])

def calculate_hypot(position1, position2):
    """calcs Euclid distance btw two points"""
    x1, y1 = position1
    x2, y2 = position2
    return hypot(x2-x1, y2-y1)


def kdtree(points):
    """Construct a k-d tree from an iterable of points.
    This algorithm is taken from Wikipedia. For more details,
    > https://en.wikipedia.org/wiki/K-d_tree#Construction
    """
    k = len(points[0])
    
    def build(*, points, depth):
        """Build a k-d tree from a set of points at a given depth.
        """
        if len(points) == 0:
            return None
        
        points.sort(key=operator.itemgetter(depth % k))
        middle = len(points) // 2
        
        return BinaryTree(
            value = points[middle],
            left = build(
                points=points[:middle],
                depth=depth+1,
            ),
            right = build(
                points=points[middle+1:],
                depth=depth+1,
            ),
        )
    return build(points=list(points), depth=0)

# NearestNeighbor = collections.namedtuple("NearestNeighbor", ["point", "distance"])

# def find_nearest_neighbor(*, tree, point):
#     """Find the nearest neighbor in a k-d tree for a given point."""
#     k = len(point)
    
#     best = None
#     def search(*, tree, depth):
#         """Recursively search through the k-d tree to find the
#         nearest neighbor.
#         """
#         nonlocal best
        
#         if tree is None:
#             return
        
#         distance = calculate_hypot(tree.value, point)
#         if best is None or distance < best.distance:
#             best = NearestNeighbor(point=tree.value, distance=distance)
        
#         axis = depth % k
#         diff = point[axis] - tree.value[axis]
#         if diff <= 0:
#             close, away = tree.left, tree.right
#         else:
#             close, away = tree.right, tree.left
        
#         search(tree=close, depth=depth+1)
#         if diff**2 < best.distance:
#             search(tree=away, depth=depth+1)
    
#     search(tree=tree, depth=0)
#     return best.point

NearestNeighbor = collections.namedtuple("NearestNeighbor", ["point", "distance"])

def find_nearest_neighbor(*, tree, point):
    """Find the nearest neighbor in a k-d tree for a given point."""
    k = len(point)
    conflicts = []

    # best = None
    def search(*, tree, depth):
        """Recursively search through the k-d tree to find the
        nearest neighbor.
        """
        # nonlocal best
        
        if tree is None:
            return
        
        distance = calculate_hypot(tree.value, point)

        if distance <= CONFLICT_RADIUS:
            conflicts.append(tree.value)
            best = NearestNeighbor(point=tree.value, distance=distance)
        

        axis = depth % k
        diff = point[axis] - tree.value[axis]
        if diff <= 0:
            close, away = tree.left, tree.right
        else:
            close, away = tree.right, tree.left
        
        search(tree=close, depth=depth+1)
        if diff**2 < best.distance:
            search(tree=away, depth=depth+1)
    
    search(tree=tree, depth=0)
    return conflicts



# def find_conflict_points(*, tree, position):
#     """MY FUNCTION _____ Find any points in conflict with each other"""
#     k = len(position)

#     def traverse(*, tree, depth):
#         """Recurse through tree to find points in a conflict zone"""


# USED TUPLES - CHANGE BACK TO LISTS
# positions = [(gen_coord(), gen_coord()) for i in range(NUM_DRONES)]
positions = [ (1, 2), (3, 2), (4, 1), (3, 5) ]
tree = kdtree(positions)
print(find_nearest_neighbor(tree=tree, point=(1500000, 1)))
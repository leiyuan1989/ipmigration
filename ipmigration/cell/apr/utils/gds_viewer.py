import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPLPolygon


class Box:
    def __init__(self, x, y, width, height, attribute, label):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.attribute = attribute
        self.label = label


class Polygon:
    def __init__(self, points, attribute, label):
        self.points = points
        self.attribute = attribute
        self.label = label


def visualize_boxes_and_polygons(shapes):
    fig, ax = plt.subplots()
    color_mapping = {
        'A': 'red',
        'B': 'blue',
        'C': 'green',
        'D': 'yellow',
        'E': 'orange',
        'F': 'purple'
    }

    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    for shape in shapes:
        if isinstance(shape, Box):
            color = color_mapping.get(shape.attribute, 'gray')
            rect = Rectangle((shape.x, shape.y), shape.width, shape.height,
                             facecolor=color, alpha=0.5)
            ax.add_patch(rect)

            center_x = shape.x + shape.width / 2
            center_y = shape.y + shape.height / 2
            ax.text(center_x, center_y, shape.label, ha='center', va='center', color='black')

            min_x = min(min_x, shape.x)
            min_y = min(min_y, shape.y)
            max_x = max(max_x, shape.x + shape.width)
            max_y = max(max_y, shape.y + shape.height)
        elif isinstance(shape, Polygon):
            color = color_mapping.get(shape.attribute, 'gray')
            poly = MPLPolygon(shape.points, facecolor=color, alpha=0.5)
            ax.add_patch(poly)

            # 计算多边形的重心以放置标签
            x_coords, y_coords = zip(*shape.points)
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            ax.text(center_x, center_y, shape.label, ha='center', va='center', color='black')

            min_x = min(min_x, min(x_coords))
            min_y = min(min_y, min(y_coords))
            max_x = max(max_x, max(x_coords))
            max_y = max(max_y, max(y_coords))

    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    ax.set_aspect('equal')
    ax.set_title('ASTRI GDS Viewer')
    plt.show()


if __name__ == "__main__":
    boxes = [
        Box(1, 1, 3, 3, 'A', 'Label A'),
        Box(2, 2, 3, 3, 'B', 'Label B'),
        Box(4, 4, 3, 3, 'C', 'Label C'),
        Box(6, 1, 2, 4, 'D', 'Label D'),
        Box(0, 5, 2, 2, 'E', 'Label E'),
        Box(3, 6, 4, 1, 'F', 'Label F')
    ]

    polygons = [
        Polygon([(7, 7), (9, 7), (8, 9)], 'A', 'Poly Label A'),
        Polygon([(1, 8), (3, 8), (2, 10)], 'B', 'Poly Label B')
    ]

    all_shapes = boxes + polygons
    visualize_boxes_and_polygons(all_shapes)
    
"""
Utility methods related to graphics.
"""

def get_polygon_area(vertices, include_perimeter=True):
    """
    Shoelace algorithm.
    """
    total = 0
    perimeter = 0
    for i, (x, y) in enumerate(vertices):
        if i == len(vertices) - 1:
            continue
        next_vertex = vertices[i + 1]
        total += x * next_vertex[1] - y * next_vertex[0]
        if include_perimeter:
            perimeter += abs(next_vertex[0] - x) + abs(next_vertex[1] - y)

    last_vertex = vertices[-1]
    first_vertex = vertices[0]
    total += last_vertex[0] * first_vertex[1] - last_vertex[1] * first_vertex[0]
    area = abs(total) / 2
    if include_perimeter:
        perimeter += (
            abs(last_vertex[0] - first_vertex[0]) +
            abs(last_vertex[1] - first_vertex[1])
        )
        area += perimeter/2 + 1
    return int(area)

def closest_point_on_triangle(p, a, b, c):
    # check edges
    p1 = closest_point_on_segment(p, a, b)
    p2 = closest_point_on_segment(p, b, c)
    p3 = closest_point_on_segment(p, c, a)

    # return nearest
    d1 = (p - p1).length()
    d2 = (p - p2).length()
    d3 = (p - p3).length()

    if d1 < d2 and d1 < d3:
        return p1
    elif d2 < d3:
        return p2
    return p3


def closest_point_on_segment(p, a, b):
    ab = b - a
    t = (p - a).dot(ab) / ab.length_squared()

    t = max(0, min(1, t))
    return a + ab * t
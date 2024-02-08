import numpy as np
from scipy.spatial import ConvexHull
import math
import pygame

def get_mid_points(p1, p2):
    return (((p1[0] + p2[0]) / 2), 
            ((p1[1] + p2[1]) / 2))

def calculate_point_section(p1, p2, per):
    x_three_quarters = (per * p1[0] + p2[0]) / 10
    y_three_quarters = (per * p1[1] + p2[1]) / 10
    three_quarters_point = (x_three_quarters, y_three_quarters)
    return three_quarters_point

def calculate_custom_point(p1, p2, perc):
    if not (0 <= perc <= 1):
        raise ValueError("Percentage must be between 0 and 1")

    x_custom_point = (1 - perc) * p1[0] + perc * p2[0]
    y_custom_point = (1 - perc) * p1[1] + perc * p2[1]
    custom_point = (x_custom_point, y_custom_point)
    return custom_point

def bezier_curve(t, points):
    n = len(points) - 1
    result = np.zeros_like(points[0])

    for i in range(n + 1):
        result += (
            math.comb(n, i) * (1 - t)**(n - i) * t**i * points[i]
        )

    return result

def get_midpoints(points, num_lines):
    center = np.mean(points, axis=0)
    midpoints = []

    for i in range(len(points)):
        point = get_mid_points(points[i], points[(i+1) % len(points)])
        midpoints.append(point)
    new_midpoints = []
    for mid in midpoints:
        scale_factor = np.random.uniform(0.5, 1.5)
        displaced = center[0] + scale_factor * (mid[0] - center[0]), center[1] + scale_factor * (mid[1] - center[1])
        new_midpoints.append(displaced)

    return new_midpoints


if __name__ == "__main__":
    num = 10
    x_values = np.random.uniform(50, 900, num)
    y_values = np.random.uniform(50, 900, num)
    points = np.column_stack((x_values, y_values)) 

    hull = ConvexHull(points)
    hull_verts = points[hull.vertices]

    new_midpoints = get_midpoints(hull_verts, 1)
    midpoints = np.array(new_midpoints)

    second_point = []
    third_points = []
    for i in range(len(hull_verts)):
        p1 = calculate_custom_point(hull_verts[i], hull_verts[(i+1) % len(hull_verts)], 0.1)
        second_point.append(p1)
        p2 = calculate_custom_point(hull_verts[i], hull_verts[(i+1) % len(hull_verts)], 0.9)
        third_points.append(p2)

    third_points = np.array(third_points)
    second_point = np.array(second_point)


    cells = 10
    all_t_values = np.linspace(0, 1, cells)
    all_points = []
    new_curves = []
    i = 0
    for point in hull_verts:
        #all_points.append(point)
        #all_points.append(second_point[i])
        #all_points.append(third_points[i])
        if i == 0:
            last = len(third_points)
            item = np.array([bezier_curve(t, [third_points[last-1], point, second_point[i]]) for t in all_t_values])
            for coord in item:
                new_curves.append(coord)
                #all_points.append(coord)
        else:
            item = np.array([bezier_curve(t, [third_points[i-1], point, second_point[i]]) for t in all_t_values])
            for coord in item:
                new_curves.append(coord)
                #all_points.append(coord)
        i += 1
    all_points = np.array(all_points)
    new_curves.append(third_points[len(third_points)-1])

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        pygame.draw.lines(screen, pygame.Color("white"), False, new_curves, 20)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
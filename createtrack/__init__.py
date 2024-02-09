import numpy as np
from scipy.spatial import ConvexHull
import math


class CreateTrack:
    def __init__(self, num_points: int = 10, x_bounds: list = [100, 100], y_bounds: list = [100,100], corner_cells: int = 10) -> None:
        self.num_points = num_points
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.corner_cells = corner_cells


    def curve_corners(self, points):
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

        inner_point = []
        outer_point = []
        for i in range(len(points)):
            rand_perc = np.random.uniform(0.1, 0.4)
            p1 = calculate_custom_point(points[i], points[(i+1) % len(points)], rand_perc)
            inner_point.append(p1)
            rand_perc = np.random.uniform(0.6, 0.9)
            p2 = calculate_custom_point(points[i], points[(i+1) % len(points)], rand_perc)
            outer_point.append(p2)
        inner_point = np.array(inner_point)
        outer_point = np.array(outer_point)

        all_t_values = np.linspace(0, 1, self.corner_cells)
        new_curves = []
        i = 0
        for point in points:
            if i == 0:
                last = len(outer_point)
                item = np.array([bezier_curve(t, [outer_point[last-1], point, inner_point[i]]) for t in all_t_values])
                for coord in item:
                    new_curves.append(coord)
            else:
                item = np.array([bezier_curve(t, [outer_point[i-1], point, inner_point[i]]) for t in all_t_values])
                for coord in item:
                    new_curves.append(coord)
            i += 1
        new_curves.append(outer_point[len(outer_point)-1])

        return new_curves

    def random_midpoint(self, points):
        def get_mid_points(p1, p2):
            return (((p1[0] + p2[0]) / 2), 
                    ((p1[1] + p2[1]) / 2))
        

        center = np.mean(points, axis=0)
        
        index = np.random.randint(0, len(points)-2)
        point = get_mid_points(points[index], points[(index+1) % len(points)])

        scale_factor = np.random.uniform(1, 0.1)
        displaced = center[0] + scale_factor * (point[0] - center[0]), center[1] + scale_factor * (point[1] - center[1])

        points = np.insert(points, index+1, displaced, 0)

        return points

    def create_racetrack(self):
        x_values = np.random.uniform(self.x_bounds[0], self.x_bounds[1], self.num_points)
        y_values = np.random.uniform(self.y_bounds[0],  self.y_bounds[1], self.num_points)
        points = np.column_stack((x_values, y_values)) 

        hull = ConvexHull(points)
        hull_verts = points[hull.vertices]
        hull_verts = self.random_midpoint(points=hull_verts)

        curves = self.curve_corners(hull_verts)
        return  curves


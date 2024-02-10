import pyray as pr
import numpy as np
import createtrack

def calculate_point_section(p1, p2, per):
    x_three_quarters = (per * p1[0] + p2[0]) / 10
    y_three_quarters = (per * p1[1] + p2[1]) / 10
    three_quarters_point = (x_three_quarters, y_three_quarters)
    return three_quarters_point


if __name__ == "__main__":
    seed = np.random.randint(0, 2**32)
    np.random.seed(seed)

    track = createtrack.CreateTrack(10,[0,100], [0,100],15,seed)
    points = track.create_racetrack(1)


    print(points)

    if 1==0:
        pr.init_window(2000, 2000, "Hello Pyray")
        pr.set_target_fps(60)
        cam = pr.Camera2D((0, 0), (0, 0), 0, 20)

        while not pr.window_should_close():
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            pr.draw_text("Seed: {}".format(seed), 10, 10, 20, pr.RAYWHITE)
            pr.begin_mode_2d(cam)
            for i in range(len(points)-1):
                pr.draw_line_ex(list(points[i]), list(points[i+1]),1, pr.RAYWHITE)
            pr.end_mode_2d(cam)
            pr.end_drawing()
        pr.close_window()        
    else:
        pr.init_window(2000, 2000, "Racetrack")
        pr.set_target_fps(60)
        cam = pr.Camera3D([0, 40, 100], [50.0, 0.0, 50.0], [0.0, 1.0, 0.0], 90.0, 0)

        while not pr.window_should_close():
            pr.update_camera(cam, pr.CAMERA_ORBITAL)
            pr.begin_drawing()
            pr.clear_background(pr.BLACK)
            pr.draw_text("Seed: {}".format(seed), 10, 10, 20, pr.RAYWHITE)
            pr.begin_mode_3d(cam)
            pr.draw_grid(500, 3.0)
            for i in range(len(points)-1):
                pr.draw_cylinder_ex(list(points[i]), list(points[i+1]), 1, 1, 6, pr.RED)
            pr.end_mode_3d(cam)
            pr.end_drawing()
        pr.close_window()  
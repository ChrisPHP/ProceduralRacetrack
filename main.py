import numpy as np
from scipy.spatial import ConvexHull
import math
import pygame

import createtrack

def calculate_point_section(p1, p2, per):
    x_three_quarters = (per * p1[0] + p2[0]) / 10
    y_three_quarters = (per * p1[1] + p2[1]) / 10
    three_quarters_point = (x_three_quarters, y_three_quarters)
    return three_quarters_point


if __name__ == "__main__":
    track = createtrack.CreateTrack(10,[50,900], [50,900],10)
    points = track.create_racetrack()

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        pygame.draw.lines(screen, pygame.Color("white"), False, points, 20)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
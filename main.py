import pygame
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

    track = createtrack.CreateTrack(10,[50,1900], [50,1900],10)
    points = track.create_racetrack()

    pygame.init()
    screen = pygame.display.set_mode((2000, 2000))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Racetrack")

    font = pygame.font.Font(None, 36)  
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        pygame.draw.aalines(screen, pygame.Color("white"), False, points)

        text_surface = font.render("Seed: {}".format(seed), True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
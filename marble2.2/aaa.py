import pygame
#import gfx

# Main Class

class Setup:

    background = gfx.Images.background
    player = gfx.Images.player

    pygame.init()

    # Configuration Variables:

    black = (0,0,0)
    white = (255,255,255)
    green = (0,255,0)
    red  = (255,0,0)
    title = "Ericson's Game"

    # Setup:

    size = [700,700]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(title)
    done = False
    clock = pygame.time.Clock()

    # Logic Variables

    x_speed = 0
    y_speed = 0
    x_speed_boost = 0
    y_speed_boost = 0
    x_coord = 350
    y_coord = 350
    screen.fill(white)

    # Main Loop:

    while done == False:

        screen.blit(background,[0,0])
        screen.blit(player,[x_coord,y_coord])

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                done = True

            if event.type == pygame.KEYDOWN:               
                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_a:
                    x_speed = -6
                    x_speed_boost = 1
                if event.key == pygame.K_d:
                    x_speed = 6
                    x_speed_boost = 2
                if event.key == pygame.K_w:
                    y_speed = -6
                    y_speed_boost = 1
                if event.key == pygame.K_s:
                    y_speed = 6
                    y_speed_boost = 2

                if event.key == pygame.K_LSHIFT:

                    if x_speed_boost == 1:
                        x_speed = -10
                    if x_speed_boost == 2:
                        x_speed = 10
                    if y_speed_boost == 1:
                        y_speed = -10
                    if y_speed_boost == 2:
                        y_speed = 10                  

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    x_speed = 0
                    x_speed_boost = 0
                if event.key == pygame.K_d:
                    x_speed = 0
                    x_speed_boost = 0
                if event.key == pygame.K_w:
                    y_speed = 0
                    y_speed_boost = 0
                if event.key == pygame.K_s:
                    y_speed = 0
                    y_speed_boost = 0

        x_coord = x_coord + x_speed
        y_coord = y_coord + y_speed

        pygame.display.flip()
        pygame.display.update()

        clock.tick(20)

    pygame.quit()
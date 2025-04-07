import pygame

pygame.init()
screen = pygame.display.set_mode((680, 480))
clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
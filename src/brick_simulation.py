import pygame
from brick_sprite import BrickSprite


def brick_simulation(
        mass_one: float,
        mass_two: float,
        velocity_one: float,
        velocity_two: float,
):
    pygame.init()
    pygame.display.set_caption("Elastic Collision Simulation")
    screen = pygame.display.set_mode((680, 480))
    clock = pygame.time.Clock()
    running = True
    is_paused = True
    dt = 0

    # init fonts and text
    hint_font = pygame.font.SysFont("monospace", 18)
    pause_hint = hint_font.render("Press space to pause/resume the simulation", True, "grey85")
    paused_text = hint_font.render("simulation paused", True, "grey85")

    cambria_math = pygame.font.SysFont("cambriamath", 16)
    m1 = cambria_math.render(f"m\u2081 = {mass_one:.2f} kg", True, "grey15")
    m2 = cambria_math.render(f"m\u2082 = {mass_two:.2f} kg", True, "grey85")

    # create brick sprites
    # noinspection PyTypeChecker
    bricks = pygame.sprite.Group(
        BrickSprite(
            mass=mass_one,
            velocity=velocity_one,
            rect=pygame.FRect(0, 100, 100, 50),
            color="red",
            screen_width=screen.width,
            image=m1
        ),
        BrickSprite(
            mass=mass_two,
            velocity=velocity_two,
            rect=pygame.FRect(screen.width - 100, 100, 100, 50),
            color="blue",
            screen_width=screen.width,
            image=m2
        )
    )

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_paused = not is_paused

        screen.fill("black")
        bricks.draw(screen)

        screen.blit(pause_hint, (screen.width // 2 - pause_hint.width // 2, screen.height - pause_hint.height))

        if not is_paused:
            bricks.update(dt)

            collisions = pygame.sprite.groupcollide(bricks, bricks, False, False)

            for brick, collision_sprites in collisions.items():
                for target_sprite in collision_sprites:
                    if brick != target_sprite:
                        brick.handle_collision(target_sprite)
        else:
            screen.blit(paused_text, (screen.width // 2 - paused_text.width // 2, 5))

        pygame.display.flip()
        dt = clock.tick(144) / 1000

    pygame.quit()
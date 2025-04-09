import pygame
from brick_sprite import BrickSprite


def _render_velocity_texts(font, brick_group: pygame.sprite.Group) -> (pygame.Surface, pygame.Surface):
    sprites = brick_group.sprites()
    return (
        font.render(f"v\u2081 = {abs(sprites[0].velocity):.2f} m/s", True, "grey85"),
        font.render(f"v\u2082 = {abs(sprites[1].velocity):.2f} m/s", True, "grey85"),
    )


def _calculate_simulation_info_pos(
        screen: pygame.Surface, m1_text: pygame.Surface, v2_text: pygame.Surface
) -> ((int, int), (int, int), (int, int), (int, int)):

    base_height = 200
    line_spacing = 5
    margin = 200

    first_col_x = margin
    second_col_x = screen.width - margin - v2_text.width
    first_row_y = base_height
    second_row_y = base_height + m1_text.height + line_spacing

    return (
        (first_col_x, first_row_y),
        (first_col_x, second_row_y),
        (second_col_x, first_row_y),
        (second_col_x, second_row_y),
    )


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

    # create brick sprites
    # noinspection PyTypeChecker
    bricks = pygame.sprite.Group(
        BrickSprite(
            mass=mass_one,
            velocity=velocity_one,
            rect=pygame.FRect(0, 100, 100, 50),
            color="red",
            screen_width=screen.width,
        ),
        BrickSprite(
            mass=mass_two,
            velocity=velocity_two,
            rect=pygame.FRect(screen.width - 100, 100, 100, 50),
            color="blue",
            screen_width=screen.width,
        )
    )

    # init fonts and text
    monospace = pygame.font.SysFont("monospace", 18)
    cambria_math = pygame.font.SysFont("cambriamath", 20)

    pause_hint = monospace.render("Press space to pause/resume the simulation", True, "grey80")
    paused_text = monospace.render("simulation paused", True, "grey85")

    m1_text = cambria_math.render(f"m\u2081 = {mass_one:.2f} kg", True, "grey85")
    m2_text = cambria_math.render(f"m\u2082 = {mass_two:.2f} kg", True, "grey85")

    v1_text, v2_text = _render_velocity_texts(cambria_math, bricks)

    m1_text_pos, v1_text_pos, m2_text_pos, v2_text_pos = _calculate_simulation_info_pos(
        screen, m1_text, v2_text
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

        # draw simulation parameters
        screen.blit(m1_text, m1_text_pos)
        screen.blit(v1_text, v1_text_pos)
        screen.blit(m2_text, m2_text_pos)
        screen.blit(v2_text, v2_text_pos)

        if not is_paused:  # Update simulation state

            bricks.update(dt)  # Update brick position

            # handle collisions
            collisions = pygame.sprite.groupcollide(bricks, bricks, False, False)

            for brick, collision_sprites in collisions.items():
                for target_sprite in collision_sprites:
                    if brick != target_sprite:

                        brick.handle_collision(target_sprite)
                        v1_text, v2_text = _render_velocity_texts(cambria_math, bricks)

        else:
            screen.blit(paused_text, (screen.width // 2 - paused_text.width // 2, 5))

        pygame.display.flip()
        dt = clock.tick(144) / 1000

    pygame.quit()
import pygame
import constants

class BrickSprite(pygame.sprite.Sprite):
    def __init__(
            self,
            mass: float,
            velocity: float,
            rect: pygame.FRect,
            color: pygame.typing.ColorLike,
            screen_width: int,
    ):
        super().__init__()

        self.mass = mass  # [kg]
        self.velocity = velocity  # [m/s]

        self.rect = rect
        self.image = pygame.Surface(rect.size)

        self.screen_width = screen_width

        self.image.fill(color)

    @property
    def kinetic_energy(self):
        return self.mass * self.velocity ** 2 / 2

    def _move(self, dt: float):

        self.rect.x += self.velocity * constants.PIXELS_PER_METER * dt

        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity *= -1
        elif self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.velocity *= -1

    def update_velocity(self, other_mass: float, other_velocity: float):
        self.velocity = (self.velocity * (self.mass - other_mass) + 2 * other_mass * other_velocity) / (
                    self.mass + other_mass)

    def move_out_of_collision(self, other: 'BrickSprite'):
        if self.rect.left < other.rect.right:  # this sprite is to the left
            self.rect.right = int(other.rect.left) - 1
        else:  # this sprite is to the right
            self.rect.left = int(other.rect.right) + 1

    def handle_collision(self, other: 'BrickSprite'):
        if not self.rect.colliderect(other.rect):
            return

        this_mass = self.mass
        this_velocity = self.velocity

        self.update_velocity(other.mass, other.velocity)
        other.update_velocity(this_mass, this_velocity)

        self.move_out_of_collision(other)

    def update(self, dt: float):
        self._move(dt)

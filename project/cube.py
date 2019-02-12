import pygame
import math

WHITE = (255, 255, 255)

class Cube(pygame.sprite.Sprite):

    direction = 50
    ball_speed = 5

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.bounce_sound = pygame.mixer.Sound('bounce.wav')
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def bounce(self, diff):
        self.bounce_sound.play()
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):

        direction_radians = math.radians(self.direction)

        self.rect.x += self.ball_speed * math.sin(direction_radians)
        self.rect.y -= self.ball_speed * math.cos(direction_radians)

        if self.rect.y <= 0:
            self.bounce(0)
            self.rect.y = 1

        if self.rect.x <= 0:
            self.bounce_sound.play()
            self.direction = (360 - self.direction) % 360
            self.rect.x = 1

        if self.rect.x > 1350:
            self.bounce_sound.play()
            self.direction = (360 - self.direction) % 360
            self.rect.x = 1349

        if self.rect.y > 780:
            return True
        else:
            return False

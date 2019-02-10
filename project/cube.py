import pygame
import math

WHITE = (255, 255, 255)

class Cube(pygame.sprite.Sprite):

    direction = 50

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
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.rect.x += 5 * math.sin(direction_radians)
        self.rect.y -= 5 * math.cos(direction_radians)

        # Do we bounce off the top of the screen?
        if self.rect.y <= 0:
            self.bounce(0)
            self.rect.y = 1

        # Do we bounce off the left of the screen?
        if self.rect.x <= 0:
            self.bounce_sound.play()
            self.direction = (360 - self.direction) % 360
            self.rect.x = 1

        # Do we bounce of the right side of the screen?
        if self.rect.x > 1350:
            self.bounce_sound.play()
            self.direction = (360 - self.direction) % 360
            self.rect.x = 1349

        # Did we fall off the bottom edge of the screen?
        if self.rect.y > 780:
            return True
        else:
            return False

    def cube_collision(self, block):
        if self.rect.x == block.rect.x + 100 and ((self.rect.y <= block.rect.y + 20 and self.rect.y >= block.rect.y) or (self.rect.y + 10 <= block.rect.y + 20 and self.rect.y + 10 >= block.rect.y)):
            self.direction = (360 - self.direction) % 360
            return True
        elif self.rect.x + 10 == block.rect.x and ((self.rect.y <= block.rect.y + 20 and self.rect.y >= block.rect.y) or (self.rect.y + 10 <= block.rect.y + 20 and self.rect.y + 10 >= block.rect.y)):
            self.direction = (360 - self.direction) % 360
            return True
        elif self.rect.y == block.rect.y + 20 and ((self.rect.x <= block.rect.x + 100 and self.rect.x >= block.rect.x) or (self.rect.x + 10 <= block.rect.x + 100 and self.rect.x + 10 >= block.rect.x)):
            self.direction = (180 - self.direction) % 360
            return True
        elif self.rect.y + 10 == block.rect.y and ((self.rect.x <= block.rect.x + 100 and self.rect.x >= block.rect.x) or (self.rect.x + 10 <= block.rect.x + 100 and self.rect.x + 10 >= block.rect.x)):
            self.direction = (180 - self.direction) % 360
            return True
        return False

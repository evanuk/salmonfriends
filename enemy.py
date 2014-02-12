import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, image, x, y, speedx, speedy, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.speedx = speedx
        self.speedy = speedy
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        self.rect.x += self.speedx * dt
        self.rect.y += self.speedy * dt

        if self.rect.left < 0 or self.rect.right > self.screen_width:
            self.speedx = -self.speedx
        if self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.speedy = -self.speedy




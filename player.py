import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, image, imageflip, x, y, speed, screen_width, screen_height):
        pygame.sprite.Sprite.__init__(self)
        #size 171x100
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y
        self.speed = speed
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.imagename = image
        self.imageflipname = imageflip
        self.imageheight = 100
        self.imagewidth = 175

    def update(self, dt):
        #check if need to be moved
        if self.move_up:
            if self.rect.top > 0:
                self.rect.y -= dt * self.speed
        if self.move_down:
            if self.rect.bottom < self.screen_height:
                self.rect.y += dt * self.speed
        if self.move_right:
            if self.rect.right < self.screen_width:
                self.rect.x += dt * self.speed
            self.image = pygame.image.load(self.imagename)
        if self.move_left:
            if self.rect.left > 0:
                self.rect.x -= dt * self.speed
            self.image = pygame.image.load(self.imageflipname)

    def grow(self, factor):
        #self.imageheight = int(self.imageheight*factor)
        #self.imagewidth = int(self.imagewidth*factor)
        bottom = self.rect.bottom
        left = self.rect.left
        self.image = pygame.transform.rotozoom(self.image, 0, factor)
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.left = left
        return self

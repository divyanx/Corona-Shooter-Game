import pygame
import random
from os import path
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,0)
YELLOW = (123,34,124)
#settings:
pygame.init()
pygame.mixer.init()
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shoot-Karona!")
clock = pygame.time.Clock()
FPS = 60
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder,"img")
#Game Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60,60))
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10  #sepration between bottom and ship
        self.speed_x = 0
        self.speed = 8
        self.last_bullet_shot = pygame.time.get_ticks()
    def shoot_bullet(self):
        current_time  = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot > 100:
            self.last_bullet_shot = current_time
            b = Bullet(self.rect.centerx, self.rect.top)
            all_bullets.add(b)
            all_sprites.add(b)


    def boundary(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def movement(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_RIGHT]:
            self.speed_x = self.speed
        if keystate[pygame.K_LEFT]:
            self.speed_x = -self.speed
        self.rect.x += self.speed_x
        if keystate[pygame.K_SPACE]:
            self.shoot_bullet()
    def update(self):
        self.movement()
        self.boundary()

class Corona(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice((corona_img))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)  #x direction motion
    def spawn_new_corona(self):
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-3, 3)  # x direction motion
    def boundary(self):
         if self.rect.left >  WIDTH + 5 or self.rect.right < -5 or self.rect.top > HEIGHT + 5:
            self.spawn_new_corona()
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(10,20))
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = -10
    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
#Game Functions
def spawn_new_corona():
    m = Corona()
    all_corona.add(m)
    all_sprites.add(m)

def get_image(filename, colorkey = None):
    img = pygame.image.load(path.join(img_folder,filename)).convert()
    img.set_colorkey(colorkey)
    return img

#images
background = get_image("background.png")
background_rect = background.get_rect()
player_img = get_image("player2.png",WHITE)  #7
bullet_img = get_image("bullet1.png",BLACK)
corona_img = []
for i in range(1,6):
    img = get_image("virus{}.png".format(i))
#player_img =
#player_img = get_image("playerShip.png")
#Game sprites
all_sprites = pygame.sprite.Group()
all_corona = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(9):
   spawn_new_corona()
#Main Game
running = True
while running:
    clock.tick(FPS)

    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update (for our sprites)
    all_sprites.update()

    #checking ship collisions
    corona_collision = pygame.sprite.spritecollide(player,all_corona,False)
    if corona_collision:
        running = False

    #checking bullet collision
    bullet_collision = pygame.sprite.groupcollide(all_corona,all_bullets,True,True)
    for collision in  bullet_collision:
        spawn_new_corona()

    #Draw/Render
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    #Update the display
    pygame.display.update()
pygame.quit()
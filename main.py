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
score = 0
font_name = pygame.font.match_font("comicsansms")
#Game Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(60,60))
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radious = int(self.rect.width*.9/2)
        #pygame.draw.circle(self.image,GREEN,self.rect.center,self.radious)
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
        self.original_image = random.choice((corona_img))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radious = int(self.rect.width * .9 / 2)
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-150,-100)
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-3,3)  #x direction motion
        self.last_rotation = pygame.time.get_ticks()
        self.rotation_degree = 0
        self.rotation_speed = 5
    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rotation  >200:
            self.last_rotation = current_time
            self.rotation_degree += self.rotation_speed
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image,self.rotation_degree)
            self.rect = self.image.get_rect()

            #pygame.draw.circle(self.image, GREEN, self.rect.center, self.radious)
            self.rect.center = old_center
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
        self.rotate()


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
def message_to_screen(message,color,font_size,x,y):
    font = pygame.font.SysFont(font_name,font_size)
    text = font.render(message,True,color)
    text_rect = text.get_rect()
    text_rect.center = (x,y)
    screen.blit(text,text_rect)

#images
background = get_image("background.png",BLACK)
background_rect = background.get_rect()
player_img = get_image("player1.png",BLACK)  #7
bullet_img = get_image("bullet1.png",BLACK)
corona_img = []
# for i in range(1,6):
#     img = get_image("virus{}.png".format(i))
#     corona_img.append(img)
for i in range(1,6):
    img = get_image("player1.png",WHITE)
    corona_img.append(img)
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
    corona_collision = pygame.sprite.spritecollide(player,all_corona,False,pygame.sprite.collide_circle)
    if corona_collision:
        running = False

    #checking bullet collision
    bullet_collision = pygame.sprite.groupcollide(all_corona,all_bullets,True,True)
    for collision in  bullet_collision:
        spawn_new_corona()
        score +=  int(int(150 - collision.radius)//10)
    #Draw/Render
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    message_to_screen("Score: "+str(score), WHITE, 24, WIDTH/2, 10)
    #Update the display
    pygame.display.update()
pygame.quit()
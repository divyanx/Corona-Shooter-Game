import pygame, sys
import random
from os import path
import pygame.mixer
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (200,200,0)
OLIVE = (128,128,0)
BRIGHT_BLUE = (21,244,238)
BRIGHT_GREEN = (102,255,0)
BRIGHT_RED = (170,1,20)
CHOCOLATE = (66,40,14)
SADDLE = (139,69,19)
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
font = pygame.font.SysFont(None, 20)
score = 0
font_name = pygame.font.match_font("comicsansms")
pause = False
bullet_sound = pygame.mixer.Sound(path.join(img_folder, "shot.mp3"))
virus_sound = pygame.mixer.Sound(path.join(img_folder, "virus.flac"))
hit_sound= pygame.mixer.Sound(path.join(img_folder, "skill_hit.mp3"))
explode_sound= pygame.mixer.Sound(path.join(img_folder, "DeathFlash.flac"))
over_sound= pygame.mixer.Sound(path.join(img_folder, "gameover.wav"))
sanatise_sound = pygame.mixer.Sound(path.join(img_folder, "enchant.ogg"))
#music

#Game Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(90,70))
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.9/2)
        #pygame.draw.circle(self.image,GREEN,self.rect.center,self.radious)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10  #sepration between bottom and ship
        self.speed_x = 0
        self.speed = 8
        self.last_bullet_shot = pygame.time.get_ticks()
        self.health = 100
        self.lives = 2
        self.hide_ship_timer = pygame.time.get_ticks()
        self.ship_is_hidden = False

    def hide_ship(self):
        self.hide_ship_timer = pygame.time.get_ticks()
        self.ship_is_hidden = True
        self.rect.centerx = WIDTH/2
        self.rect.y = -1000
    def shoot_bullet(self):
        current_time  = pygame.time.get_ticks()
        if current_time - self.last_bullet_shot > 300:
            self.last_bullet_shot = current_time
            b = Bullet(self.rect.centerx, self.rect.top)
            all_bullets.add(b)
            all_sprites.add(b)
            bullet_sound.play(100,900)


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
        if self.ship_is_hidden and pygame.time.get_ticks() - self.hide_ship_timer > 1500:
            self.ship_is_hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-10
        self.movement()
        self.boundary()

class Corona(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imsize = random.randrange(3,8)*19
        self.original_image = pygame.transform.scale(random.choice((corona_img)),(imsize,imsize))
        #self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        if score < 500:
            self.rect.x = random.randrange(1, 10)*(WIDTH )/10 - self.rect.width
            self.rect.y = random.randrange(-150, -100)
            self.speed_y = 4
            self.speed_x = 0 # x direction motion
        else:
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-150,-100)
            self.speed_y = random.randrange(2,8) + score/500
            self.speed_x = random.randrange(-1,2)  #x direction motion
        self.last_rotation = pygame.time.get_ticks()
        self.rotation_degree = 0
        self.rotation_speed = random.randrange(1,7)
    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rotation  >50:
            self.last_rotation = current_time
            self.rotation_degree += self.rotation_speed
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image,self.rotation_degree)
            self.rect = self.image.get_rect()

            #pygame.draw.circle(self.image, GREEN, self.rect.center, self.radious)
            self.rect.center = old_center
    def spawn_new_corona(self):
        # self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # self.rect.y = random.randrange(-150, -100)
        # self.speed_y = random.randrange(2, 8)
        # self.speed_x = random.randrange(-3, 3)  # x direction motion
        if score < 500:
            self.rect.x = random.randrange(1, 10) * (WIDTH ) / 10 - self.rect.width
            self.rect.y = random.randrange(-150, -100)
            self.speed_y = 4
            self.speed_x = 0  # x direction motion
        else:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speed_y = random.randrange(2, 8) + score / 500
            self.speed_x = random.randrange(-1, 2)  # x direction motion
    def boundary(self):
         if self.rect.left >  WIDTH + 5 or self.rect.right < -5 or self.rect.top > HEIGHT + 5:
            self.spawn_new_corona()
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()
        self.rotate()
class boss_corona(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imsize = random.randrange(2,5)*15
        self.original_image = pygame.transform.scale(random.choice((corona_img)),(imsize,imsize))
        #self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)

        self.rect.center = mainboss.rect.center
        self.speed_y = random.randrange(2,8)
        self.speed_x = random.randrange(-8,8)


        self.last_rotation = pygame.time.get_ticks()
        self.rotation_degree = 0
        self.rotation_speed = random.randrange(1,7)
    def rotate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rotation  >50:
            self.last_rotation = current_time
            self.rotation_degree += self.rotation_speed
            old_center = self.rect.center
            self.image = pygame.transform.rotate(self.original_image,self.rotation_degree)
            self.rect = self.image.get_rect()

            #pygame.draw.circle(self.image, GREEN, self.rect.center, self.radious)
            self.rect.center = old_center
    def spawn_new_boss(self):
        # self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # self.rect.y = random.randrange(-150, -100)
        # self.speed_y = random.randrange(2, 8)
        # self.speed_x = random.randrange(-3, 3)  # x direction motion

        self.rect.center = mainboss.rect.center
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-8, 8)

    def boundary(self):
         if self.rect.left >  WIDTH + 5 or self.rect.right < -5 or self.rect.top > HEIGHT + 5:
            self.spawn_new_boss()
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
class Sanetiser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(sanatiser_img,(50,90))
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speed_y = random.randrange(5, 15)
        self.speed_x = random.randrange(-3, 3)  # x direction motion
        self.last_bullet_shot = pygame.time.get_ticks()
        self.hide_sanatiser_timer = pygame.time.get_ticks()
        self.sanatiser_is_hidden = False
    def hide_sanatiser(self):
        self.hide_sanatiser_timer = pygame.time.get_ticks()
        self.sanatiser_is_hidden = True
        self.rect.centerx = random.randrange(0, WIDTH -self.rect.width)
        self.rect.y = -100

    def boundary(self):
         if self.rect.left >  WIDTH + 5 or self.rect.right < -5 or self.rect.top > HEIGHT + 5:
            self.hide_sanatiser()
    def update(self):
        if(self.sanatiser_is_hidden == False):
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x

        if self.sanatiser_is_hidden and pygame.time.get_ticks() - self.hide_sanatiser_timer > 15000:
            self.sanatiser_is_hidden = False
            self.rect.centerx = random.randrange(0, WIDTH - self.rect.width)
            self.speed_y = random.randrange(5, 15)
            self.speed_x = 0
        self.boundary()

class Explosion(pygame.sprite.Sprite):
    def __init__(self,expl_size,center):
        pygame.sprite.Sprite.__init__(self)
        self.expl_size = expl_size
        self.image = self.expl_size[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pygame.time.get_ticks()
        self.current_frame = 0
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame > 40:
            self.last_frame = current_time
            self.current_frame +=1
            if(self.current_frame == len(self.expl_size)):
                self.kill()
            else:
                old_center = self.rect.center
                self.image = self.expl_size[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        imsize = 200
        self.image = pygame.transform.scale(boss_img,(imsize,int(imsize*1.3)))
        #self.image = pygame.transform.scale(bullet_img, (10, 20))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        if score > 100:
            self.rect.x = random.randrange(100,WIDTH-100)
            self.rect.y = random.randrange(150, 200)
            self.speed_y = random(-2,2)
            self.speed_x = random(-3,3) # x direction motion
        else:
            self.rect.x = random.randrange(100,WIDTH-100)
            self.rect.y = random.randrange(-450,-300)
            self.speed_y = 0
            self.speed_x = 0  #x direction motion
        self.i = 1
    def spawn_boss_corona(self):
        self.currenttime = pygame.time.get_ticks()
        if self.currenttime - self.lastfire > 5000:
            self.rect.center = mainboss.rect.center
        # self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        # self.rect.y = random.randrange(-150, -100)
        # self.speed_y = random.randrange(2, 8)
        # self.speed_x = random.randrange(-3, 3)  # x direction motion

    def boundary(self):
        if score>100:
             if self.rect.left >  WIDTH - 100:
                self.speed_x = random.randrange(-3,-1)
             if  self.rect.right < 100 :
                self.speed_x = random.randrange(1, 3)
             if self.rect.bottom < 200:
                 self.speed_y = random.randrange(1,3)
             if self.rect.top > HEIGHT/2:
                 self.speed_y = random.randrange(-3, -1)

    def update(self):


        # if score < 100:
        #     self.rect.x = random.randrange(100,WIDTH-100)
        #     self.rect.y = random.randrange(-400, -300)
        #     self.speed_y = 0
        #     self.speed_x = 0  # x direction motion
        # else:
        #     self.rect.x = random.randrange(100,WIDTH-100)
        #     self.rect.y = random.randrange(150, 200)
        #     self.speed_y = random.randrange(-2,2)
        #     self.speed_x = random.randrange(-2,2)  # x direction motion
        if score > 100 and self.i > 0:
            pygame.mixer.music.load(path.join(img_folder, "boss.wav"))
            pygame.mixer.music.play(-1)
            self.i-=1
            self.rect.x = random.randrange(100, WIDTH - 100)
            self.rect.y = random.randrange(150, 200)
            self.speed_y = random.randrange(1, 2)
            self.speed_x = random.randrange(1, 3)  # x direction motion
        if score > 100:
            self.lastfire = pygame.time.get_ticks()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        self.boundary()
#Game Functions
click = False
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    clk = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1]>y:
        pygame.draw.rect(screen,ac,(x,y,w,h))
        if clk[0]==1 and action!=None:
            if action == "play":
                new_game()
            elif action == "quit":
                pygame.quit()
            elif action == "intro":
                #print("#here2")
                game_intro()
            elif action == "menu":
                game_intro()
            elif action == "pause":
                paused()
            elif action == "unpause":
                unpaused()
    else:
        pygame.draw.rect(screen,ic,(x,y,w,h))
    smalltext = pygame.font.Font("freesansbold.ttf",20)
    textsurf, textrect = text_objects(msg,smalltext)
    textrect.center = ((x+(w/2)),(y+(h/2)))
    screen.blit(textsurf,textrect)
def draw_text(text,fonts,color,surface,x,y):
    textobj = fonts.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)
def game_intro():
    pygame.mixer.music.load(path.join(img_folder, "menumusic.mp3"))
    pygame.mixer.music.play(-1)
    global click
    intro = True
    while intro:
        screen.blit(main_menu_bg,(0,0))
        largetext = pygame.font.Font('freesansbold.ttf', 60)
        TextSurf, TextRect = text_objects("Shoot Karona!!", largetext)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 2 - 200))
        screen.blit(TextSurf, TextRect)
        button("START",WIDTH/2-75,HEIGHT/2-50,150,50,BLUE,BRIGHT_BLUE,"play")
        button("QUIT",WIDTH/2-75,HEIGHT/2+50,150,50,RED,BRIGHT_RED,"quit")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        pygame.display.update()
        pygame.time.Clock().tick(60)
        #largeText = pygame.font.Font('freesansbold.ttf',115)
def new_game():
    pygame.mixer.music.load(path.join(img_folder, "gamemenu.mp3"))
    pygame.mixer.music.play(-1)
    global score
    score = 0
    player.lives = 2
    player.health = 100
    game()
def spawn_new_corona():
    m = Corona()
    all_corona.add(m)
    all_sprites.add(m)
    all_boss_normal.add(m)
def span_new_boss_corona():
    c = boss_corona()
    all_boss_corona.add(c)
    all_sprites.add(c)
    all_boss_normal.add(c)
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
def text_objects(text,font):
    textsurface = font.render(text,True,WHITE)
    return textsurface,textsurface.get_rect()
def paused():
    pygame.mixer.music.load(path.join(img_folder, "pausemenu.mp3"))
    pygame.mixer.music.play(-1)
    global pause
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                sys.exit()
        screen.blit(start_page_background,(0,0))
        largetext = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("PAUSED",largetext)
        TextRect.center = ((WIDTH/2),(HEIGHT/2-200))
        screen.blit(TextSurf,TextRect)
        button("CONTINUE",25,400,150,50,GREEN,BRIGHT_GREEN,"unpause")
        button("RESTART",225,400,150,50,BLUE,BRIGHT_BLUE,"play")
        button("MAIN MENU",425,400,150,50,OLIVE,YELLOW,"menu")
        pygame.display.update()
        clock.tick(30)

def unpaused():
    pygame.mixer.music.load(path.join(img_folder, "gamemenu.mp3"))
    pygame.mixer.music.play(-1)
    global pause
    pause = False

def game_over():
    global score
    over_sound.play()
    pygame.mixer.music.load(path.join(img_folder, "gameover.mp3"))
    pygame.mixer.music.play(-1)
    global click
    game_over  = True
    while game_over:
        screen.blit(main_menu_bg, (0, 0))

        largetext = pygame.font.Font('freesansbold.ttf', 80)
        stext = pygame.font.Font('freesansbold.ttf',60)
        TextSurf, TextRect = text_objects("GAME OVER!!", largetext)
        TextRect.center = ((WIDTH / 2), (HEIGHT / 2 - 200))
        stextSurf, stextRect = text_objects("Your Score is "+str(score),stext)
        stextRect.center = ((WIDTH / 2), (HEIGHT / 2 - 100))
        screen.blit(TextSurf, TextRect)
        screen.blit(stextSurf,stextRect)
        #print("here")
        button("MAIN MENU", WIDTH / 2 - 75, HEIGHT / 2 - 50, 150, 50, BLUE, BRIGHT_BLUE, "intro")
        button("QUIT", WIDTH / 2 - 75, HEIGHT / 2 + 50, 150, 50, RED, BRIGHT_RED, "quit")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        pygame.display.update()
        pygame.time.Clock().tick(60)
#images
background = get_image("background1.png",BLACK)
background_rect = background.get_rect()
player_img = get_image("player1.png",WHITE)  #7
bullet_img = get_image("bullet1.png",BLACK)
boss_img = get_image("boss.png",WHITE)
sanatiser_img = get_image("sanatiser.png",WHITE)
start_page_background = get_image("start_page.jpg",WHITE)
main_menu_bg = get_image("main_menu_bg.jpg", WHITE)
corona_img = []
small_explosion = []
large_explosion = []
ship_explosion = []
sanatised = []
for i in range(1,11):
    img = get_image("virus{}.png".format(i),WHITE)
    corona_img.append(img)
for i in range(11,18):
    img = get_image("virus{}.png".format(i),BLACK)
    corona_img.append(img)
for i in range(1,9):
    img = get_image("h{}.png".format(i), WHITE)
    sanatised.append(pygame.transform.scale(img,(50,50)))
for i in range(1,7):
    img = get_image("ex{}.png".format(i),WHITE)
    large_explosion.append(pygame.transform.scale(img,(80,80)))
    small_explosion.append(pygame.transform.scale(img, (40, 40)))
for i in range(1,6):
    img = get_image("se{}.png".format(i),WHITE)
    ship_explosion.append(pygame.transform.scale(img, (100, 100)))
#player_img =
#player_img = get_image("playerShip.png")
#Game sprites
all_sprites = pygame.sprite.Group()
all_corona = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()
all_boss_corona = pygame.sprite.Group()
all_boss_normal = pygame.sprite.Group()
player = Player()
mainboss = Boss()
sanatiser = Sanetiser()
all_sprites.add(player)
all_sprites.add(sanatiser)
all_sprites.add(mainboss)
for i in range(9):
   spawn_new_corona()
for i in range(10):
   span_new_boss_corona()
#Main Game
def game():
    pygame.mixer.music.load(path.join(img_folder, "gamemenu.mp3"))
    pygame.mixer.music.play(-1)
    global score
    global radius
    running = True
    while running:
        clock.tick(FPS)

        #check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    paused()
                if event.key == pygame.K_x:
                    pygame.quit()
        #Update (for our sprites)
        all_sprites.update()

        #checking ship collisions
        corona_collision = pygame.sprite.spritecollide(player,all_corona,True,pygame.sprite.collide_circle)
        for hit in  corona_collision:
            hit_sound.play()
            expl = Explosion(small_explosion,player.rect.center)
            all_sprites.add(expl)
            player.health -= int(hit.radius*0.2)
            spawn_new_corona()

            #final_explosion = Explosion(ship_explosion, player.rect.center)
            if player.health <= 0:
                explode_sound.play()
                final_explosion = Explosion(ship_explosion,player.rect.center)
                all_sprites.add(final_explosion)
                player.hide_ship()
                player.health = 100
                player.lives -= 1
            if player.lives <= 0:
                game_over()
        boss_corona_collision = pygame.sprite.spritecollide(player, all_boss_corona, True, pygame.sprite.collide_circle)
        for hit in boss_corona_collision:
            hit_sound.play()
            expl = Explosion(small_explosion, player.rect.center)
            all_sprites.add(expl)
            player.health -= int(hit.radius * 0.2)
            span_new_boss_corona()

            # final_explosion = Explosion(ship_explosion, player.rect.center)
            if player.health <= 0:
                explode_sound.play()
                final_explosion = Explosion(ship_explosion, player.rect.center)
                all_sprites.add(final_explosion)
                player.hide_ship()
                player.health = 100
                player.lives -= 1
            if player.lives <= 0:
                game_over()

        #checking bullet collision
        bullet_collision = pygame.sprite.groupcollide(all_corona,all_bullets,True,True)
        for collision in bullet_collision:
            expl = Explosion(large_explosion,collision.rect.center)
            virus_sound.play(200, 1000)
            all_sprites.add(expl)
            spawn_new_corona()
            score +=  int((100 - collision.radius)/11)
        boss_corona_bullet_collision = pygame.sprite.groupcollide(all_boss_corona, all_bullets, True, True)
        for collision in boss_corona_bullet_collision:
            expl = Explosion(large_explosion, collision.rect.center)
            virus_sound.play(200, 1000)
            all_sprites.add(expl)
            span_new_boss_corona()
            score += int((100 - collision.radius) / 11)

        get_sanatiser = pygame.sprite.collide_circle(sanatiser,player)
        if get_sanatiser:
            got = Explosion(sanatised,player.rect.center)
            sanatise_sound.play()
            all_sprites.add(got)
            sanatiser.hide_sanatiser()
            player.health += 50
            if player.health > 100:
                player.health = 100

        #Draw/Render
        screen.blit(background,background_rect)
        all_sprites.draw(screen)
        message_to_screen("Score: "+str(score), WHITE, 24, WIDTH/2, 10)
        message_to_screen("Health: "+str(player.health),WHITE,24,70,10)
        message_to_screen("Life:" + str(player.lives), WHITE, 24, 178, 10)
        message_to_screen("Playing", RED, 24, 550, 780)
        message_to_screen("Press SPACE to shoot <- -> to move", OLIVE, 24, 139, 35)
        #Update the display
        button("Pause(P)", 400, 0, 100, 30, CHOCOLATE, SADDLE, "pause")
        button("Exit(X)",500,0 ,100,30,CHOCOLATE,SADDLE,"quit")
        pygame.display.update()

    pygame.quit()

game_intro()
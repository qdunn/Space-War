# Imports
import pygame
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1000
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

level = 5

# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
WALL_TEXT =(204, 0, 102)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (179, 182, 188)
DARKGRAY = (124, 126, 130)
BLUE = (16, 68, 188)
DARKBLUE = (7, 38, 109)
BHEALTH = (168, 3, 154)
GREEN = (100, 255, 100)
MOON_STAR = (244, 238, 173)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
pause_screen = pygame.font.Font("assets/fonts/Fonts/Samuels.ttf", 50)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)
continue_text = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 70)

# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
ship_up = pygame.image.load('assets/images/player_up.png').convert_alpha()
ship_right = pygame.image.load('assets/images/player_left.png').convert_alpha()
ship_left = pygame.image.load('assets/images/player_right.png').convert_alpha()

ship_small = pygame.image.load('assets/images/player_small.png').convert_alpha()
ship_small_up = pygame.image.load('assets/images/player_small_up.png').convert_alpha()
ship_small_right = pygame.image.load('assets/images/player_small_left.png').convert_alpha()
ship_small_left = pygame.image.load('assets/images/player_small_right.png').convert_alpha()

laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()

green_enemy1 = pygame.image.load('assets/images/NewPiskel.png').convert_alpha()
green_enemy2 = pygame.image.load('assets/images/anim.png').convert_alpha()

long_enemy1 = pygame.image.load('assets/images/long.png').convert_alpha()
long_enemy2 = pygame.image.load('assets/images/long_switch.png').convert_alpha()

teth_enemy1 = pygame.image.load('assets/images/teth.png').convert_alpha()
teth_enemy2 = pygame.image.load('assets/images/teth_switch.png').convert_alpha()

stach_enemy1 = pygame.image.load('assets/images/stach.png').convert_alpha()
stach_enemy2 = pygame.image.load('assets/images/stach_switch.png').convert_alpha()

small_meteor_img = pygame.image.load('assets/images/meteorSmall.png').convert_alpha()
big_meteor_img = pygame.image.load('assets/images/meteorBig.png').convert_alpha()
ouch_ship_img = pygame.image.load('assets/images/playerDamaged.png').convert_alpha()
powerup_img = pygame.image.load('assets/images/laserGreenShot.png').convert_alpha()
bigbad = pygame.image.load('assets/images/bous.png').convert_alpha()

hold = 0

# Space Objects
num_stars = 2000
stars = []
for i in range(num_stars):
     x = random.randrange(0, WIDTH)
     y = random.randrange(0, HEIGHT)
     s = [x, y , 1, 1]
     stars.append(s)

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
shoot = pygame.mixer.Sound('assets/sounds/shoot.ogg')
alien = pygame.mixer.Sound('assets/sounds/alien.ogg')
hit = pygame.mixer.Sound('assets/sounds/hit.wav')
start1 = pygame.mixer.Sound('assets/sounds/Start.ogg')
start2 = pygame.mixer.Sound('assets/sounds/New Start.wav')
end = pygame.mixer.Sound('assets/sounds/end.ogg')


# Stages
START = 0
PLAYING = 1
END = 2
CONTINUE = 3
WIN = 4
PAUSE = 5

# Game classes
        
class HealthPowerup(pygame.sprite.Sprite):
     def __init__(self, x, y, image):
          super().__init__()
        
          self.image = image
          self.rect = self.image.get_rect()
          self.mask = pygame.mask.from_surface(self.image)
          self.rect.x = x
          self.rect.y = y
          self.speed = 6

     def apply(self, ship):
          if ship.health < 6:
               ship.health += 1

     def update(self):
          self.rect.y += self.speed
          
class InvincPowerup(pygame.sprite.Sprite):
     def __init__(self, x, y, image):
          super().__init__()
        
          self.image = image
          self.invinc = 0
          self.rect = self.image.get_rect()
          self.mask = pygame.mask.from_surface(self.image)
          self.rect.x = x
          self.rect.y = y
          self.speed = 6

     def apply(self, ship):
          while self.invinc < 5:
               self.invinc += 1/60
               ship.health = ship.health

     def update(self):
          self.rect.y += self.speed

class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

        self.speed = 3*(1000/800)
        self.health = 6

    def move_left(self):
        if (self.image == ship_small or
            self.image == ship_small_right or
            self.image == ship_small_up):
             
          self.image = ship_small_left
          self.mask = pygame.mask.from_surface(ship_small_left)
             
                   
        elif (self.image == ship_img or
              self.image == ship_up or
              self.image == ship_right):
             
          self.image  = ship_left
          self.mask = pygame.mask.from_surface(ship_left)
          
        self.rect.x -= self.speed
        
    def adjust(self):
        #print(self.rect.left)
         
        if self.rect.right > WIDTH:
             self.rect.right = WIDTH
        
        if self.rect.left < 0:
             self.rect.left = 0
             
        
        if self.rect.top < HEIGHT/2:
             self.rect.top = HEIGHT/2

        if (self.image == ship_img or
             self.image == ship_right or
             self.image == ship_up or
             self.image == ship_left) and self.rect.bottom > HEIGHT:
                  self.rect.bottom = HEIGHT

        if (self.image == ship_small or
            self.image == ship_small_right or
            self.image == ship_small_up or
            self.image == ship_small_left) and self.rect.bottom > HEIGHT + (75/2):
             
             self.rect.bottom = HEIGHT +(75/2)
             
    def stop(self):
         if (self.image == ship_small or
             self.image == ship_small_right or
             self.image == ship_small_up or
             self.image == ship_small_left):
              
              self.image = ship_small
              self.mask = pygame.mask.from_surface(ship_small)
              
         if (self.image == ship_img or
             self.image == ship_right or
             self.image == ship_up or
             self.image == ship_left):
              
              self.image = ship_img
              self.mask = pygame.mask.from_surface(ship_img)
    
    def move_right(self):
        if (self.image == ship_small or
            self.image == ship_small_left or
            self.image == ship_small_up):
             
          self.image = ship_small_right
          self.mask = pygame.mask.from_surface(ship_small_right)
             
                   
        elif (self.image == ship_img or
              self.image == ship_up or
              self.image == ship_left):
          self.image  = ship_right
          self.mask = pygame.mask.from_surface(ship_right)
          
        self.rect.x += self.speed

    def move_up(self):
        if self.image == ship_small:
          self.image = ship_small_up
             
                   
        elif self.image == ship_img:
          self.image  = ship_up
                        
                   
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        self.damage = 1
        if (self.image == ship_small or
            self.image == ship_small_left or
            self.image == ship_small_up or
            self.image == ship_small_right):

             self.damage = 1/2
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

        if self.image == ship_small:

             laser.rect.centerx = self.rect.centerx - 25
             laser.rect.centery = self.rect.top

    def shrink(self):
         if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_s:
                     self.image = ship_small
                     self.speed = 7.5
                     self.mask = pygame.mask.from_surface(ship_small)
                     
              if event.key == pygame.K_a:
                     self.image = ship_img
                     self.speed = 3*(1000/800)
                     self.mask = pygame.mask.from_surface(ship_img)

    def update(self):
        global stage

        self.adjust()
        self.shrink()
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            
        hot_list = pygame.sprite.spritecollide(self, powerups, True,
                                              pygame.sprite.collide_mask)
        
        for hits in hot_list:
             hits.apply(self)
             hit.play()

        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        hort_lorst = pygame.sprite.spritecollide(self, projectiles, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
             self.health -= 1
             hit.play()

        if len(hort_lorst) > 0:
             self.health -= 1
             hit.play()
             
        if self.health == 0:
             self.kill()
             end.play()
             stage = END
             
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()


        hit_list = pygame.sprite.spritecollide(self, projectiles, True,
                                               pygame.sprite.collide_mask)
        if len(hit_list) > 0:
             self.kill()
        
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 1
        self.health = 2
        self.moving_right = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        
    def drop_bomb(self):
        
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx - 5
        bomb.rect.bottom = self.rect.bottom
        bombs.add(bomb)
        
    def move(self):
         hits_edge = False
         for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                self.image = green_enemy2

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed
                self.image = green_enemy1

                if m.rect.left <= 0:
                    hits_edge = True
                    
         if hits_edge:
              self.reverse()
              
    def reverse(self):
        self.moving_right = not self.moving_right
        
    def update(self):
        self.move()
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= ship.damage
            if self.health <= 0:
                 self.kill()
                 alien.play()
                 player.score += 2
            
class Stach(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.moving_right = True
        self.rect = image.get_rect()
        self.health = 1
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        
    def drop_bomb(self):
        
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx - 5
        bomb.rect.bottom = self.rect.bottom
        bombs.add(bomb)
    def move(self):
         hits_edge = False
         for m in stachs:
            if self.moving_right:
                m.rect.x += self.speed
                self.image = stach_enemy2

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed
                self.image = stach_enemy1

                if m.rect.left <= 0:
                    hits_edge = True
         if hits_edge:
              self.reverse()
              
    def reverse(self):
        self.moving_right = not self.moving_right
        
    def update(self):
        self.move()
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= ship.damage
            if self.health <= 0:
                 self.kill()
                 alien.play()
                 player.score += 1
            
class Long(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.health = 4
        self.speed = 1
        self.moving_right = True
        self.rect = image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        
    def drop_bomb(self):
        
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx - 5
        bomb.rect.bottom = self.rect.bottom
        bombs.add(bomb)
        
    def move(self):
         hits_edge = False
         for m in longs:
            if self.moving_right:
                m.rect.x += self.speed
                self.image = long_enemy2

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed
                self.image = long_enemy1

                if m.rect.left <= 0:
                    hits_edge = True
                    
         if hits_edge:
              self.reverse()
              
    def reverse(self):
        self.moving_right = not self.moving_right
        
    def update(self):
        self.move()
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= ship.damage
            if self.health <= 0:
                 self.kill()
                 alien.play()
                 player.score += 3

class Teth(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.health = 3
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.moving_right = True
        self.rect.y = y
        
    def drop_bomb(self):
        
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx - 5
        bomb.rect.bottom = self.rect.bottom
        bombs.add(bomb)
        
    def move(self):
         hits_edge = False
         for m in teths:
            if self.moving_right:
                m.rect.x += self.speed
                self.image = teth_enemy2

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed
                self.image = teth_enemy1

                if m.rect.left <= 0:
                    hits_edge = True
                    
         if hits_edge:
              self.reverse()
              
    def reverse(self):
        self.moving_right = not self.moving_right
        
    def update(self):
        self.move()
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= ship.damage
            if self.health <= 0:
                 self.kill()
                 alien.play()
                 player.score += 4
            
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.health = 100
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.moving_right = True
        self.rect.y = y
        
    def drop_bomb(self):
        images = [small_meteor_img, big_meteor_img]
        
        projectile = Projectile(random.choice(images))
        projectile.rect.centerx = self.rect.centerx - 5
        projectile.rect.bottom = self.rect.bottom
        projectiles.add(projectile)
        
    def move(self):
         hits_edge = False
         for m in boss:
            if self.moving_right:
                m.rect.x += self.speed
                self.image = bigbad

                if m.rect.right >= WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed
                self.image = bigbad

                if m.rect.left <= 0:
                    hits_edge = True
                    
         if hits_edge:
              self.reverse()
              
    def reverse(self):
        self.moving_right = not self.moving_right
        
    def update(self):
        self.move()
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)
        
        if len(hit_list) > 0:
            self.health -= ship.damage
            if self.health <= 0:
                 self.kill()
                 alien.play()
                 player.score += 4
            
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
class Projectile(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 3

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            
class Fleet():
    def __init__(self, mobs):
        super().__init__()
        
        self.mobs = mobs
        if level == 1:
             self.bomb_rate = 60
             
        if level == 2:
             self.bomb_rate = 50
             
        if level == 3:
             self.bomb_rate = 40
             
        if level == 4:
             self.bomb_rate = 30

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop
            
        for m in longs:
             m.rect.y += self.drop

        for m in teths:
             m.rect.y += self.drop

        for m in stachs:
             m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()
        long_list = longs.sprites()
        stach_list = stachs.sprites()
        teth_list = teths.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
            
        if len(long_list) > 0 and rand == 0:
            bomber = random.choice(long_list)
            bomber.drop_bomb()

        if len(stach_list) > 0 and rand == 0:
            bomber = random.choice(stach_list)
            bomber.drop_bomb()

        if len(teth_list) > 0 and rand == 0:
            bomber = random.choice(teth_list)
            bomber.drop_bomb()
    
    def update(self):
        self.choose_bomber()
        print(self.bomb_rate)
        
class BigBadFleet():
    def __init__(self, mobs):
        super().__init__()
        
        self.mobs = mobs
        self.bomb_rate = 30
        
    def move_down(self):
        for m in boss:
            m.rect.y += self.drop

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        boss_list = boss.sprites()

        if len(boss_list) > 0 and rand == 0:
            bomber = random.choice(boss_list)
            bomber.drop_bomb()
    
    def update(self):
        self.choose_bomber()
        
# Game helper functions
def draw_stars():
    for s in stars:
         pygame.draw.ellipse(screen, MOON_STAR, s)
         s[0] += 1
         s[1] += 1
         if s[0] > WIDTH:
             s[0] = 0
         if s[1] > HEIGHT:
             s[1] = 0

def draw_health():
    pygame.draw.line(screen, DARKGRAY, [0, HEIGHT - 50], [165, HEIGHT - 50], 10)
    pygame.draw.line(screen, DARKGRAY, [160, HEIGHT - 50], [160, HEIGHT], 10)
    pygame.draw.rect(screen, GRAY, [1, HEIGHT - 49, 60+99, 50])
    pygame.draw.rect(screen, GREEN, [1, HEIGHT - 49, ship.health*(159/6), 50])
    pygame.draw.line(screen, DARKGRAY, [0, HEIGHT], [165, HEIGHT], 10)
    pygame.draw.line(screen, DARKGRAY, [0, HEIGHT - 50], [0, HEIGHT], 10)
    
def draw_boss_health():
    pygame.draw.line(screen, DARKBLUE, [WIDTH/2+84.5, 0], [WIDTH/2+84.5, 50], 10)
    pygame.draw.rect(screen, BLUE, [WIDTH/2-78.5, 1, 60+99, 50])
    pygame.draw.rect(screen, BHEALTH, [WIDTH/2-78.5, 1, boss1.health*(159/100), 50])
    pygame.draw.line(screen, DARKBLUE, [WIDTH/2-79.5, 0], [WIDTH/2+79.5, 0], 10)
    pygame.draw.line(screen, DARKBLUE, [WIDTH/2-83.5, 50], [WIDTH/2+89.5, 50], 10)
    pygame.draw.line(screen, DARKBLUE, [WIDTH/2-79.5, 0], [WIDTH/2-79.5, 50], 10)
    
def show_end():
    global level

    level = 1
    text1 = pause_screen.render("GAME OVER", True, WALL_TEXT)
    w = text1.get_width()
    h = text1.get_height()
    screen.blit(text1, [WIDTH/2 -w/2, HEIGHT/2 -h/2])

    text2 = pause_screen.render("(Press space to play again.)", True, WALL_TEXT)
    w = text2.get_width()
    screen.blit(text2, [WIDTH/2 -w/2, 400])
    
def show_pause():
    text1 = pause_screen.render("Paused", True, WALL_TEXT)
    w = text1.get_width()
    h = text1.get_height()
    screen.blit(text1, [WIDTH/2 -w/2, HEIGHT/2 -h/2])

    text2 = pause_screen.render("(Press P to play.)", True, WALL_TEXT)
    w = text2.get_width()
    screen.blit(text2, [WIDTH/2 -w/2, 400])

def show_win():
    text1 = pause_screen.render("You Win!!!", True, WALL_TEXT)
    w = text1.get_width()
    h = text1.get_height()
    screen.blit(text1, [WIDTH/2 -w/2, HEIGHT/2 -h/2])

    text2 = pause_screen.render("Press space to play again", True, WALL_TEXT)
    w = text2.get_width()
    screen.blit(text2, [WIDTH/2 -w/2, 400])
    
def place():
     global stage
     stage = CONTINUE
     
     title_text = continue_text.render("You are on level " + str(level-1) +" !", True, WHITE)
     screen.blit(title_text, [10, 204])
     
     text2 = continue_text.render("Press any button to Advance", 1, WHITE)
     screen.blit(text2, [10, 254])
    
def show_title_screen():
    global sounds
    
    sounds = [start1, start2]
    
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    screen.blit(title_text, [128, 204])

        
def show_stats():
    global level
    
    '''health'''
    score_textt = FONT_XL.render(str(ship.health), 1, WHITE)
    score_rectt = score_textt.get_rect()
    score_rectt.left = 20
    score_rectt.top = 20
    screen.blit(score_textt, score_rectt)
    
    '''level'''
    score_textt = FONT_XL.render(str(level), 1, WHITE)
    score_rectt = score_textt.get_rect()
    score_rectt.right = WIDTH - 20
    score_rectt.top = 20
    screen.blit(score_textt, score_rectt)
    
def check_win():
     global stage, level

     if len(player) == 0:
          stage = END
          
     elif level < 5 and (len(mobs) == 0 and len(teths) == 0 and
           len(longs) == 0 and len(stachs) == 0): 
          level += 1
          stage = CONTINUE
     elif len(boss) == 0:
          stage = WIN
          
def setup():
    global stage, done
    global player, ship, lasers, mobs, bombs, longs, teths, stachs, powerups, boss
    global floet, fleot, foeet, fleet, bossfleet
    global boss, boss1, bossfleet, projectiles
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH/2
    ship.rect.bottom = HEIGHT

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    
    
    mob1 = Mob(100, 100, green_enemy2)
    mob2 = Mob(300, 100, green_enemy2)
    mob3 = Mob(500, 100, green_enemy2)
    mob4 = Mob(700, 100, green_enemy2)
    mob6 = Long(200, 50, long_enemy2)
    mob7 = Long(400, 50, long_enemy2)
    mob8 = Long(600, 50, long_enemy2)
    mob9 = Long(800, 50, long_enemy2)
    mob10 = Teth(200, 150, teth_enemy2)
    mob11 = Teth(400, 150, teth_enemy2)
    mob12 = Teth(600, 150, teth_enemy2)
    mob13 = Teth(800, 150, teth_enemy2)
    mob14 = Stach(100, 200, stach_enemy2)
    mob15 = Stach(300, 200, stach_enemy2)
    mob16 = Stach(500, 200, stach_enemy2)
    mob17 = Stach(700, 200, stach_enemy2)
    powerup1 = HealthPowerup(WIDTH/2, -2000, powerup_img)
    powerup2 = InvincPowerup(WIDTH/2, -1000, powerup_img)
    boss1 = Boss(0, 0, bigbad)
    

    mobs = pygame.sprite.Group()
    longs = pygame.sprite.Group()
    teths = pygame.sprite.Group()
    stachs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    boss = pygame.sprite.Group()

    
    fleet = Fleet(mobs)
    fleot = Fleet(longs)
    floet = Fleet(teths)
    foeet = Fleet(stachs)
    bossfleet = BigBadFleet(boss)

        
    mobs.add(mob1, mob2, mob3, mob4)
    longs.add(mob6, mob7, mob8, mob9)
    teths.add(mob10, mob11, mob12, mob13)
    stachs.add(mob14, mob15, mob16, mob17)
    boss.add(boss1)
    powerups.add(powerup1,powerup2)

    ''' set stage '''
    stage = START
    done = False


# Game loop
setup()
while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                 done = True
                 
            if stage == START:
                if event.key == pygame.K_SPACE and level < 5:
                    stage = PLAYING
                    
                    pygame.mixer.music.load("assets/sounds/Background.ogg")
                    pygame.mixer.music.play(-1)
                    random.choice(sounds).stop()
                    
                if event.key == pygame.K_SPACE and level == 5:
                    stage = PLAYING
                    pygame.mixer.music.load("assets/sounds/bous.ogg")
                    pygame.mixer.music.play(-1)
                    random.choice(sounds).stop()
                    
                random.choice(sounds).play()

            elif stage == CONTINUE and level == 5:
                 setup()
                 start1.stop()
                 start2.stop()
                 pygame.mixer.music.load("assets/sounds/bous.ogg")
                 pygame.mixer.music.play(-1)

                 
                 if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == CONTINUE and level < 5:
                 setup()
                 start1.stop()
                 start2.stop()
                 pygame.mixer.music.load("assets/sounds/bous.ogg")
                 pygame.mixer.music.play(-1)

                 if event.key == pygame.K_SPACE:
                      stage = PLAYING
                 
            elif stage == PLAYING:
                start1.stop()
                start2.stop()
                
                    
                if event.key == pygame.K_p:
                    stage = PAUSE
                    
                if event.key == pygame.K_r:
                    setup()
                    
                     
                if event.key == pygame.K_SPACE:
                    shoot.play()
                    ship.shoot()
               
                    
            elif stage == PAUSE:
                    if event.key == pygame.K_p:
                        stage = PLAYING

            elif stage == END:
                if event.key == pygame.K_SPACE:
                    end.stop()
                    setup()
            elif stage == WIN:
                 if event.key == pygame.K_SPACE:
                      setup()
                        
        
    pressed = pygame.key.get_pressed()
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        else:
             ship.stop()
            
        if pressed[pygame.K_UP]:
            ship.move_up()
        elif pressed[pygame.K_DOWN]:
            ship.move_down()
        check_win()
            
        player.update()
        lasers.update()
        bombs.update()
        powerups.update()
        
        if level <5:
             fleet.update()
             mobs.update()
             longs.update()
             teths.update()
             stachs.update()
             
        if level == 5:
             bossfleet.update()
             boss.update()
             projectiles.update()
             
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    draw_stars()
    lasers.draw(screen)
    
    if level < 5:
         mobs.draw(screen)
         longs.draw(screen)
         teths.draw(screen)
         stachs.draw(screen)
         bombs.draw(screen)
         
    if level == 5:
        boss.draw(screen)
        projectiles.draw(screen)
        draw_boss_health()
    
    player.draw(screen)
    powerups.draw(screen)
    show_stats()
    draw_health()
    
    if stage == START:
        show_title_screen()
    elif stage == PAUSE:
        show_pause()
    elif stage == CONTINUE:
          place()
    elif stage == END:
        pygame.mixer.music.stop()
        show_end()
    elif stage == WIN:
         show_win()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()

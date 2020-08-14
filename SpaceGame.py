
import pygame
import random
import os
import time

pygame.font.init()

WIDTH,HEIGHT = 600,600

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("SPACE INVADERS")

vel1 = 5


# load images

RED_SPACE_SHIP = pygame.image.load("pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load("pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("pixel_ship_blue_small.png")


YELLOW_SPACE_SHIP = pygame.image.load("pixel_ship_yellow.png") #Player Ship

# LASERs
RED_LASER = pygame.image.load("pixel_laser_red.png")
GREEN_LASER = pygame.image.load("pixel_laser_green.png")
BLUE_LASER = pygame.image.load("pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("pixel_laser_yellow.png")

#Background
BACKGROUND = pygame.image.load("background-black.png")
BG = pygame.transform.scale(BACKGROUND, (WIDTH,HEIGHT))

class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self, image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    


class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health = 60):
        self.x = x
        self.y = y
        self.health = health
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_laser(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
            

    def shoot(self):
        if self.cool_down_counter == 0:
            laser == Laser(self.x, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_don_counter += 1
            

    def get_width(self):
        return self.ship_image.get_width()

    def get_height(self):
        return self.ship_image.get_width()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_image = YELLOW_SPACE_SHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)
        self.max_health = health

        
    def move_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
              

class Invader(Ship):
    SHIP_COLORS = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
        }
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_image, self.laser_image = self.SHIP_COLORS[color]
        self.mask = pygame.mask.from_surface(self.ship_image)

        

    def move(self, vel):
        self.y += vel
        
    def shoot(self):
        if self.cool_down_counter == 0:
            laser == Laser(self.x - 20, self.y, self.laser_image)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 2
    lost = False
    lost_count = 0
    laser_vel = 5
    LETTER_FONT = pygame.font.SysFont('comicsans', 40)
    LOST_FONT = pygame.font.SysFont("comicsans", 60)

    invaders = []

    wave_length = 5
    invader_vel = 1
    clock = pygame.time.Clock()

    player = Player(300, 550)

    def redraw_window():
        win.blit(BG, (0,0))

        lives_label = LETTER_FONT.render(f"Lives: {lives}", 1, (255, 255, 255))
        levels_label = LETTER_FONT.render(f"Level: {level}", 1, (255, 255, 255))

        win.blit(lives_label, (10, 10))
        win.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        
        for invader in invaders:
            invader.draw(win)
            
        player.draw(win)

        if lost:
            lost_label = LOST_FONT.render("You Lost!!!!", 1, (255,255,255))
            win.blit(lost_label,(WIDTH/2 - int(lost_label.get_width()/2), WIDTH/2) )
            

        
        pygame.display.update()
    
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue
            

        if len(invaders) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                invader = Invader(random.randrange(50, WIDTH-100), random.randrange(-1500*level/5, -100), random.choice(["red", "blue", "green"]))
                invaders.append(invader)
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x > vel1: #Left
            player.x -= vel1
        if keys[pygame.K_d] and player.x + vel1 + player.get_width() < WIDTH : #Right
            player.x += vel1
        if keys[pygame.K_w] and player.y - vel1 > 0: #Up
            player.y -= vel1
        if keys[pygame.K_s] and player.y + vel1 + player.get_height() < HEIGHT: #Down
            player.y += vel1

        if keys[pygame.K_SPACE]:
            player.shoot()
        

        for invader in invaders[:]:
            invader.move(invader_vel)
            invader.move_lasers(laser_vel, player)

            if randow.randrange(0, 2*60) == 1:
                invader.shoot()
                
            if invader.y +invader.get_height() > HEIGHT:
                lives -= 1
                invaders.remove(invader)

        player.move_lasers(-laser_vel, invaders)
        


main()        

pygame.quit()


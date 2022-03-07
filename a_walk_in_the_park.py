import pygame
import random
pygame.init()

screen_width = 1280
screen_height = 720

win = pygame.display.set_mode((screen_width, screen_height))
win.set_alpha(100)
pygame.display.set_caption('a walk in the park')

clock = pygame.time.Clock()

font_80 = pygame.font.Font('font/arcadeclassic.ttf', 80)
font_100 = pygame.font.Font('font/arcadeclassic.ttf', 100)
font_120 = pygame.font.Font('font/arcadeclassic.ttf', 120)

game_time = 0
score = 0
high_score = 0

background = [0, 0, 0, 0]
background_image = []
for i in range (0, 4):
    background_image.append(pygame.image.load('sprites/bg/bg000' + str(i) + '.png'))

#colors
score_blue = (30, 100, 240)
game_over_red = (200, 0, 40)
slime_green = (0, 250, 187)

#sound
music = pygame.mixer.music.load('sound/exploration.mp3')
pygame.mixer.music.play(-1)

jumpSound = pygame.mixer.Sound('sound/slime_jump.wav')
landSound = pygame.mixer.Sound('sound/slime_land.wav')
fallSound = pygame.mixer.Sound('sound/slime_fall.wav')

space_pressed = False

player_walk = []
for i in range (0, 6):
    player_walk.append(pygame.image.load('sprites/player/walk000' + str(i) + '.png'))

player_jump = []
for i in range (0, 7):
    player_jump.append(pygame.image.load('sprites/player/jump000' + str(i) + '.png'))

class player:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.grounded = True
        self.vsp = 0
        self.air_time = 0
        self.ground_time = 0

    def jump(self):
        if self.grounded == True:
            self.vsp = 27
            self.grounded = False
            jumpSound.play()
            global space_pressed
            space_pressed = True

    def fall(self):
        if self.grounded == False:
            if space_pressed == False:
                if self.vsp > -6:
                    self.vsp = -7
                    global score
                    score += 20
                    fallSound.play()

    def gravity(self):
        if self.grounded == False:
            self.vsp -= 1
            self.y -= self.vsp
            
            self.air_time += 1
            self.ground_time = 0
        else:
            self.air_time = 0
            self.ground_time += 1
            
        if self.y >= screen_height - self.height + self.vsp:
            self.grounded = True
            self.vsp = 0
            self.y = screen_height - self.height
        elif self.grounded == True:
            self.grounded = False

        if self.ground_time == 1 and game_time > 20:
            landSound.play()


    def draw(self):
        if self.grounded == True:
            win.blit(player_walk[(self.ground_time // 6) % len(player_walk)], (self.x, self.y))
        else:
            if self.vsp >= 0:
                win.blit(player_jump[(27 - self.vsp) // 9], (self.x, self.y))
            else:
                if ((self.vsp * -1) // 9) + 3 > 6:
                    win.blit(player_jump[5], (self.x, self.y))
                else:
                    win.blit(player_jump[((self.vsp * -1) // 9) + 3], (self.x, self.y))
        pygame.draw.rect(win, (200, 0, 0), (self.x, self.y, self.width, self.height), 1)


obstacle_sprite = []
for s in range (0, 8):
    obstacle_sprite.append(pygame.image.load('sprites/obstacles/obstacle000' + str(s) + '.png'))
class obstacle:
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.width = 150
        self.height = 500
        self.sprite = 0
        self.lowest_distance = 10000
        self.distance = 0
        self.biggest_x = screen_width

    def movement(self):
        if game_time <= 120:
            pass
        else:
            self.x -= hsp

            if self.x < 0 - self.width: #to far left
                self.sprite = random.randrange(0, len(obstacle_sprite)) #randomizing sprite
                self.biggest_x = screen_width
                for o in obstacles:
                    if o.x > self.biggest_x:
                        self.biggest_x = o.x
                self.x = self.biggest_x + self.width + random.randrange(100, 400)

                global previous_y
                previous_y = random.randrange(previous_y - 70, previous_y + 90)
                if previous_y > screen_height - 30:
                    previous_y = screen_height - 60
                if previous_y < screen_height - 400:
                    previous_y = screen_height - 380
                self.y = previous_y

    def collision(self):
        if self.x > player.x - self.width - hsp and self.x < player.x + player.width:
            if self.y + player.vsp <= player.y + player.height:
                if self.y + 30 > player.y + player.height:
                    player.y = self.y - player.height
                    player.vsp = 0
                    player.grounded = True
                    
                else:
                    global lose
                    lose = True

    def draw(self):
        win.blit(obstacle_sprite[self.sprite], (self.x - 70, self.y - 60))
        pygame.draw.rect(win, (0, 220, 0), (self.x, self.y, self.width, self.height), 1)
                            

def draw():
    #background
    for j in range (0, len(background)):
        background[j] -= hsp / 12 * (j + 1)
        if background[j] < (screen_width * (-1)):
            background[j] = 0
        win.blit(background_image[j], (background[j], 0))
        win.blit(background_image[j], (background[j] + screen_width, 0))

    for o in obstacles:
        o.draw()

    player.draw()

def draw_with_shadow(text, x, y, color, font_size):
    if font_size == 80:
        font = font_80
    elif font_size == 100:
        font = font_100
    elif font_size == 120:
        font = font_120
    else:
        font = font_80

    black_text = font.render(text, 1, (0, 0, 0))
    if x == 'middle':
        x = (screen_width - black_text.get_width()) / 2
    win.blit(black_text, (x + 5, y + 5))
    final_text = font.render(text, 1, color)
    win.blit(final_text, (x, y))
    
player = player(150, 0, 120, 110)

run = True
title_screen = True
lose = False
lose_screen = False

while run == True:    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    if title_screen == True:
        obstacles = []
        for i in range (0, 6):
            obstacles.append(obstacle(0 + 50 * i, screen_height + 200, i))
        hsp = 5
        previous_y = screen_height / 2 + 200
        score = 0

        title_screen = False
        lose_screen = False

    if lose == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            player.jump()
            player.fall()
        elif space_pressed == True:
            space_pressed = False

        player.gravity()

        for o in obstacles:
            o.movement()
            o.collision()
        hsp += 0.005

        score += 1
        game_time += 1
        draw()

        if game_time < 300:
            if game_time < 120:
                draw_with_shadow('Press  Space  to  jump', 40, 100, slime_green, 80)
            else:
                draw_with_shadow('Press  Space  to  jump', 40 + 720 - game_time * 6, 100, slime_green, 80)

        if game_time >= 120:
            if game_time < 550:
                if game_time < 240:
                    draw_with_shadow('Press  Space  again  to  fall', 40, 170, slime_green, 80)
                else:
                    draw_with_shadow('Press  Space  again  to  fall', 40 + 1440 - game_time * 6, 170, slime_green, 80)

        draw_with_shadow('Score  ' + str(score), 40, 15, score_blue, 80)
        
        pygame.display.update()
        clock.tick(60)

    if lose == True and lose_screen == False:
        draw()
        if score > high_score:
            high_score = score

        #wrtie stuff
        draw_with_shadow('Game  Over', 'middle', 180, game_over_red, 120)

        draw_with_shadow('Press  R  to  restart', 'middle', 280, slime_green, 80)
        draw_with_shadow('Press  ESC  to  exit', 'middle', 330, slime_green, 80)

        draw_with_shadow('Score  ' + str(score) + '    High Score  ' + str(high_score), 'middle', 400, score_blue, 80)

        pygame.display.update()
        pressed = False
        lose_screen = True

    if lose_screen == True:
        keys = pygame.key.get_pressed()      
        if keys[pygame.K_r]:
            lose = False
            title_screen = True
        if keys[pygame.K_ESCAPE]:
            run = False
        clock.tick(30)
pygame.quit()

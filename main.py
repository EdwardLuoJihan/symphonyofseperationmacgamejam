import pygame, sys
import pygame.midi
from pygame.locals import *
import mido
import time
from pygame import mixer
import random
import math
import os

pygame.init()
screen = pygame.display.set_mode((1300, 800))
pygame.display.set_caption('Symphony of Seperation')
wn = pygame.Surface((1300, 800))
he = pygame.Surface((1300, 800))
hl = pygame.Surface((1300, 800))
mixer.init()
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Minecraft', 20)

#any other variables
screen_shake = 0
screen_shake3 = 0
screen_shake4 = 0
screen_shake2 = [0,0]
default_shake = 25
left_scene_bounds = [30,420,35,750]
right_scene_bounds = [865,1240,40,740]
mainclock = pygame.time.Clock()
aparticles = {
    "smallbg":[],
    "largetiles":[],
    "icons": []
}
mixer.music.load('assets/sounds/riverflowsinyou.mp3')
mixer.music.load('assets/sounds/boom.wav')
mixer.music.set_volume(0.2)
accumulated_speed = [0,0]
current = -1 #0 demon, 1 angel
sprite_width = 20

#image load
#tile dimensions - 64 x 143
#border dimensions - 350 x 800
#23 x 77 for tile spawn within border
ptileimg = "assets/images/tile.png"
pborder = "assets/images/purgborder.png"
hborder = "assets/images/heavenborder.png"
hlborder = "assets/images/hellborder.png"

border = pygame.image.load(pborder).convert_alpha()
wn.blit(border, (475, 0))

ptile = pygame.image.load(ptileimg).convert_alpha()
# wn.blit(ptile, (475+23, 77))

hborder = pygame.image.load(hborder).convert_alpha()
wn.blit(hborder, (0, 0))

hlborder = pygame.image.load(hlborder).convert_alpha()
wn.blit(hlborder, (825, 0))



#piano tiles
class Tile(pygame.sprite.Sprite):
    def __init__(self, column):
        self.y = -143
        self.vis = True
        self.column = column
        if column == 1:
            self.x = 498
        elif column == 2:
            self.x = 578
        elif column == 3:
            self.x = 659
        elif column == 4:
            self.x = 740
        self.image = ptile
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        if self.vis:
            wn.blit(tile_surf((20, 20, 60), self.x, self.y), ((self.x, self.y)), special_flags=BLEND_RGB_ADD)
            wn.blit(self.image,(self.x,self.y))

    def move(self,speedy):
        self.y += speedy

    def getpos(self):
        return self.x, self.y
    
    def v(self, vis):
        self.vis = vis

tile_group = []

#particle system

def circle_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def tile_surf(color, x, y):
    surf = pygame.Surface((64, 143))
    pygame.draw.rect(surf, color, (x, y, 64, 143), 0)
    surf.set_colorkey((0, 0, 0))
    return surf

def create_particle(minx, maxx, my, color, velocity, direction, duration, sizemin, sizemax, t):
    global screen_shake
    global screen_shake2
    global current
    if t == 1:
        aparticles["smallbg"].append([[random.randint(minx, maxx), my], [random.randint(0, velocity) / 10 - 1, -2], duration, random.randint(sizemin, sizemax)])
    
    for particle in aparticles["smallbg"]:
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        if t == 1:
            particle[3] -= 0.01
        elif t == 2:
            particle[3] -= .1
        #particle[1][1] += 0.1 gravity
        pygame.draw.circle(wn, color, [int(particle[0][0]), int(particle[0][1])], int(particle[3]))
        radius = particle[3] * 2
        wn.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
        if particle[2] <= 0 or particle[3] <= 0:
            aparticles["smallbg"].remove(particle)
    if t == 2:
        aparticles["largetiles"].append([[random.randint(minx, maxx), my], [random.randint(0, velocity) / 10 - 1, -2], duration, random.randint(sizemin, sizemax), color])
    if t == 3:
        aparticles["icons"].append([[random.randint(minx, maxx), my], [random.randint(0, velocity) / 10 - 1, -2], duration, random.randint(sizemin, sizemax), color])

    for particle in aparticles["largetiles"]:
        if particle[0][1] <= 20:
            if particle[4] == (255, 33, 122):
                mx, my = pygame.mouse.get_pos()
                if mx <= 675:
                    screen_shake2[0] += 10
                    if accumulated_speed[0] > 0:
                        accumulated_speed[0] -= 1
                    current = 0
                else:
                    screen_shake2[1] += 10
                    if accumulated_speed[1] > 0:
                        accumulated_speed[1] -= 1
                    current = 1
                #print("recieved red orb - penalize player")
            else:
                #print("recieved purple orb - move player")
                mx, my = pygame.mouse.get_pos()
                if mx <= 675:
                    screen_shake2[0] += 20
                    accumulated_speed[0] += 1
                    current = 0
                else:
                    screen_shake2[1] += 20
                    accumulated_speed[1] += 1
                    current = 1
            aparticles["largetiles"].remove(particle)
        else:
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            if t == 1:
                particle[3] -= 0.01
            elif t == 2:
                particle[3] -= .1
            #particle[1][1] += 0.1 gravity
            pygame.draw.circle(wn, particle[4], [int(particle[0][0]), int(particle[0][1])], int(particle[3]))
            radius = particle[3] * 2
            wn.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
            if particle[2] <= 0 or particle[3] <= 0:
                aparticles["largetiles"].remove(particle)


    for particle in aparticles["icons"]:
        pygame.draw.circle(screen, particle[4], [int(particle[0][0]), int(particle[0][1])], int(particle[3]))
        radius = particle[3] * 2
        screen.blit(circle_surf(radius, (20, 20, 60)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)

class GhostPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, img=None):
        super().__init__()
        self.x = x
        self.y = y
        self.speedx = 0
        self.speedy = 0
        self.image = pygame.Surface([20, 20])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def goto(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
 
    def update(self, x, y):
        self.x += x
        self.y += y
        self.rect.x += x
        self.rect.y += y

    def move(self, t):
        old_x, old_y = self.x, self.y

        # Update the position based on speed
        self.x += self.speedx
        self.y += self.speedy

        # Update the rectangle's position as well
        self.rect.x = self.x
        self.rect.y = self.y

        if t == 1:
            # Ensure player stays within left scene borders
            if self.x < left_scene_bounds[0]:
                self.x = left_scene_bounds[0]
                self.rect.x = self.x
            elif self.x > left_scene_bounds[1]:
                self.x = left_scene_bounds[1]
                self.rect.x = self.x
        if t == 2:
            # Ensure player stays within right scene borders
            if self.x < right_scene_bounds[0]:
                self.x = right_scene_bounds[0]
                self.rect.x = self.x
            elif self.x > right_scene_bounds[1]:
                self.x = right_scene_bounds[1]
                self.rect.x = self.x

        if t == 1:
            # Ensure player stays within top scene borders
            if self.y < left_scene_bounds[2]:
                self.y = left_scene_bounds[2]
                self.rect.y = self.y
            elif self.y > left_scene_bounds[3]:
                self.y = left_scene_bounds[3]
                self.rect.y = self.y

        if t == 2:
            # Ensure player stays within bottom scene borders
            if self.y < right_scene_bounds[2]:
                self.y = right_scene_bounds[2]
                self.rect.y = self.y
            elif self.y > right_scene_bounds[3]:
                self.y = right_scene_bounds[3]
                self.rect.y = self.y

        # Reduce speed over time
        self.speedx *= 0.8
        self.speedy *= 0.8
        
    def push(self, speed, x, y, mx, my):
        dx = mx - (x+(sprite_width/2))
        dy = my - (y+(sprite_width/2))
        angle = math.degrees(math.atan2(dy, dx)) * -1
        self.speedx += speed * math.cos(math.radians(angle))
        self.speedy += speed * -1 * math.sin(math.radians(angle))

    def getpos(self):
        return self.x, self.y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img=None):
        super().__init__()
        self.x = x
        self.y = y
        self.speedx = 0
        self.speedy = 0
        self.image = pygame.Surface([20, 20])
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def goto(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
 
    def update(self, x, y):
        self.x += x
        self.y += y
        self.rect.x += x
        self.rect.y += y

    def move(self, t):
        old_x, old_y = self.x, self.y

        # Update the position based on speed
        self.x += self.speedx
        self.y += self.speedy

        # Update the rectangle's position as well
        self.rect.x = self.x
        self.rect.y = self.y

        if t == 1:
            # Ensure player stays within left scene borders
            if self.x < left_scene_bounds[0]:
                self.x = left_scene_bounds[0]
                self.rect.x = self.x
            elif self.x > left_scene_bounds[1]:
                self.x = left_scene_bounds[1]
                self.rect.x = self.x
        if t == 2:
            # Ensure player stays within right scene borders
            if self.x < right_scene_bounds[0]:
                self.x = right_scene_bounds[0]
                self.rect.x = self.x
            elif self.x > right_scene_bounds[1]:
                self.x = right_scene_bounds[1]
                self.rect.x = self.x

        if t == 1:
            # Ensure player stays within top scene borders
            if self.y < left_scene_bounds[2]:
                self.y = left_scene_bounds[2]
                self.rect.y = self.y
            elif self.y > left_scene_bounds[3]:
                self.y = left_scene_bounds[3]
                self.rect.y = self.y

        if t == 2:
            # Ensure player stays within bottom scene borders
            if self.y < right_scene_bounds[2]:
                self.y = right_scene_bounds[2]
                self.rect.y = self.y
            elif self.y > right_scene_bounds[3]:
                self.y = right_scene_bounds[3]
                self.rect.y = self.y

        # Reduce speed over time
        self.speedx *= 0.8
        self.speedy *= 0.8
    
    def push(self, speed, x, y, mx, my):
        dx = mx - (x+(sprite_width/2))
        dy = my - (y+(sprite_width/2))
        angle = math.degrees(math.atan2(dy, dx)) * -1
        self.speedx += speed * math.cos(math.radians(angle))
        self.speedy += speed * -1 * math.sin(math.radians(angle))

    def getpos(self):
        return self.x, self.y

def draw_dashed_line(surface, color, start_pos, end_pos, distance, dash_length=10, gap_length=5):
    # Calculate the components of the line segment
    delta_x = end_pos[0] - start_pos[0]
    delta_y = end_pos[1] - start_pos[1]
    line_distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    
    # Calculate unit vectors for direction
    unit_x = delta_x / line_distance
    unit_y = delta_y / line_distance

    # Calculate the endpoint position based on the desired distance
    end_pos = (start_pos[0] + distance * unit_x, start_pos[1] + distance * unit_y)

    # Draw the dashed line
    x, y = start_pos
    remaining_distance = distance
    while remaining_distance > 0:
        # Calculate dash end point
        dash_end_x = x + min(dash_length, remaining_distance) * unit_x
        dash_end_y = y + min(dash_length, remaining_distance) * unit_y
        if x > 675:
            if dash_end_x <= right_scene_bounds[1] and dash_end_x >= right_scene_bounds[0] and dash_end_y >= right_scene_bounds[2] and dash_end_y <= right_scene_bounds[3]:
                pygame.draw.line(surface, color, (x, y), (dash_end_x, dash_end_y), 2)
                # Move to the next dash start point
                x = dash_end_x + gap_length * unit_x
                y = dash_end_y + gap_length * unit_y
                remaining_distance -= (dash_length + gap_length)
            else:
                break
        else:
            if dash_end_x <= left_scene_bounds[1] and dash_end_x >= left_scene_bounds[0] and dash_end_y >= left_scene_bounds[2] and dash_end_y <= left_scene_bounds[3]:
                pygame.draw.line(surface, color, (x, y), (dash_end_x, dash_end_y), 2)
                # Move to the next dash start point
                x = dash_end_x + gap_length * unit_x
                y = dash_end_y + gap_length * unit_y
                remaining_distance -= (dash_length + gap_length)
            else:
                break

player = Player(57, 720)
player2 = Player(890, 720)
players = pygame.sprite.Group()
players2 = pygame.sprite.Group()
players.add(player)
players2.add(player2)
linemaker = GhostPlayer(57, 720)
linemaker2 = GhostPlayer(890, 720)
players.add(linemaker)
players2.add(linemaker2)

levels = [
    [
        [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1],
            [1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
            [1,1,4,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
            [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,0,0,1,1,4,4,4,4,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,1,0,0,1,1,4,4,4,4,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,4,4,4,4,4,1,1],
            [1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,4,4,4,4,4,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
            [1,1,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        [

        ]
    ]
]
# for y,i in enumerate(levels[0][0]):
#     for x,j in enumerate(i):
#         if j == 0:
#             block = Player(0+x*20, 0+y*20, y)
#             players.add(block)

# for i in range(40):
#     for j in range(23):
#         player = Player(1300-j*20, 0+i*20, i)
#         players.add(player)

from beats import detect_beats

level = 0
idx = 0

bpm = 143

songbeats = [
    #detect_beats("assets/sounds/riverflowsinyou.mp3", bpm, (3,4), 3.08 * 60, .03)
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

length = 60/bpm * 1000

tilespeed = ((143/(60/bpm))/(60))
pygame.time.set_timer(pygame.USEREVENT, int(length))  # Convert to milliseconds

sya = pygame.mixer.Sound('assets/sounds/riverflowsinyou.mp3')

#music played
music_played = False
icons_made = [False, False]

wn.set_colorkey((0, 0, 0))
he.set_colorkey((0, 0, 0))
hl.set_colorkey((0, 0, 0))


while True:
        if not pygame.mixer.get_busy():
            music_played = False
        wn.fill((0,0,0,0))
        screen.fill((0,0,0))
        he.fill((0,0,0))
        hl.fill((0,0,0))

        #move counter
        #print(player.x, player.y, player2.x, player2.y)
        if not icons_made[0]:
            create_particle(65, 65, 65, (84, 16, 148), 20, 0, 80, 10, 10, t=3)
            icons_made[0] = True
        if not icons_made[1]:
            create_particle(900, 900, 65, (84, 16, 148), 20, 0, 80, 10, 10, t=3)
            icons_made[1] = True


        #text for move
        if screen_shake2[0] > 0:
            screen_shake2[0] -= 1
        
        if screen_shake2[1] > 0:
            screen_shake2[1] -= 1

        render_offset2 = [0,0,0,0]
        if screen_shake2[0]:
            render_offset2[0] = random.randint(0, 8) - 4
            render_offset2[1] = random.randint(0, 8) - 4
        if screen_shake2[1]:
            render_offset2[2] = random.randint(0, 8) - 4
            render_offset2[3] = random.randint(0, 8) - 4

        text_surface = my_font.render(str(accumulated_speed[0]), False, (255, 255, 255))
        screen.blit(text_surface, (90+render_offset2[0], 58+render_offset2[1]))
        text_surface = my_font.render(str(accumulated_speed[1]), False, (255, 255, 255))
        screen.blit(text_surface, (930+render_offset2[2], 58+render_offset2[3]))

        #particle
        create_particle(500, 800, 722, (129, 71, 189), 30, -2, 80, 4, 5, t=1)
        
        events = pygame.event.get()

        c1 = [i for i in tile_group if i.column == 1]
        c2 = [i for i in tile_group if i.column == 2]
        c3 = [i for i in tile_group if i.column == 3]
        c4 = [i for i in tile_group if i.column == 4]

        for tile in tile_group:
            x, y = tile.getpos()
            c = tile.column
            if y >= 420 and not music_played:
                pygame.mixer.Channel(0).play(sya)
                music_played = True
            if y >= 780:
                match c:
                    case 1:
                        c1.remove(tile)
                    case 2:
                        c2.remove(tile)
                    case 3:
                        c3.remove(tile)
                    case 4:
                        c4.remove(tile)
                tile_group.remove(tile)
                tile.v(False)
                screen_shake = default_shake
                create_particle(x, x+50, y, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                mixer.music.set_volume(0.2)
                mixer.music.play()

            tile.move(tilespeed)
            tile.draw()
        
        #line
        mx, my = pygame.mouse.get_pos()
        lx, ly = linemaker.getpos()
        l2x, l2y = linemaker2.getpos()
        x, y = player.rect.x, player.rect.y
        x2, y2 = player2.rect.x, player2.rect.y
        linemaker.goto(x,y)
        linemaker2.goto(x2,y2)
        try:
            if mx < left_scene_bounds[1] and mx > left_scene_bounds[0] and my > left_scene_bounds[2] and my < left_scene_bounds[3]:
                linemaker.push(accumulated_speed[0], x, y, mx, my)
                d = math.sqrt((lx-x)**2+(ly-y)**2)
                draw_dashed_line(he, (255,255,255), (x+(sprite_width/2), y+(sprite_width/2)), (lx+(sprite_width/2),ly+(sprite_width/2)), d)
                linemaker2.push(accumulated_speed[1], x2, y2, x2+(lx-x)+(sprite_width/2), y2+(ly-y)+(sprite_width/2))
                d2 = math.sqrt((l2x-x2)**2+(l2y-y2)**2)
                draw_dashed_line(he, (255,255,255), (x2+(sprite_width/2), y2+(sprite_width/2)), (l2x+(sprite_width/2),l2y+(sprite_width/2)), d2)
            elif mx < right_scene_bounds[1] and mx > right_scene_bounds[0] and my > right_scene_bounds[2] and my < right_scene_bounds[3]:
                linemaker2.push(accumulated_speed[1], x2, y2, mx, my)
                d2 = math.sqrt((l2x-x2)**2+(l2y-y2)**2)
                draw_dashed_line(hl, (255,255,255), (x2+(sprite_width/2), y2+(sprite_width/2)), (l2x+(sprite_width/2),l2y+(sprite_width/2)), d2)
                linemaker.push(accumulated_speed[0], x, y, x+(l2x-x2)+(sprite_width/2), y+(l2y-y2)+(sprite_width/2))
                d = math.sqrt((lx-x)**2+(ly-y)**2)
                draw_dashed_line(hl, (255,255,255), (x+(sprite_width/2), y+(sprite_width/2)), (lx+(sprite_width/2),ly+(sprite_width/2)), d)
        except:
            pass

        #bounds for clicking area: ymin = 510 ymax = 725

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if sum(accumulated_speed) > 0:
                    if mx <= 675:
                        x, y = player.x, player.y
                        player.push(accumulated_speed[0], x, y, mx, my)
                        player2.push(accumulated_speed[1], x, y, mx, my)
                        if accumulated_speed[1] > 0:
                            screen_shake4 = 30
                        accumulated_speed = [0,0]
                        screen_shake3 = 30
                    else:
                        x, y = player2.x, player2.y
                        player.push(accumulated_speed[0], x, y, mx, my)
                        player2.push(accumulated_speed[1], x, y, mx, my)
                        if accumulated_speed[0] > 0:
                            screen_shake3 = 30
                        accumulated_speed = [0,0]
                        screen_shake4 = 30

            if event.type == pygame.KEYDOWN:
                mixer.music.set_volume(0.2)
                if event.key == pygame.K_z: #1
                    try:
                        tile = c1[0]
                        x, y = tile.getpos()
                        if y >= 510 and y <= 725:
                        #if 1:
                            tile_group.remove(tile)
                            c1.remove(tile)
                            tile.v(False)
                            #screen_shake = default_shake
                            create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                            #mixer.music.play()
                        else:
                            screen_shake = 5
                            create_particle(496, 496+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                            mixer.music.set_volume(0.1)
                            mixer.music.play()
                    except:
                        screen_shake = 5
                        create_particle(496, 496+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                        mixer.music.set_volume(0.1)
                        mixer.music.play()
                if event.key == pygame.K_x: #2
                    try:
                        tile = c2[0]
                        x, y = tile.getpos()
                        if y >= 510 and y <= 725:
                        #if 1:
                            tile_group.remove(tile)
                            c2.remove(tile)
                            tile.v(False)
                            #screen_shake = default_shake
                            create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                            #mixer.music.play()
                        else:
                            screen_shake = 5
                            create_particle(578, 678+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                            mixer.music.set_volume(.1)
                            mixer.music.play()
                    except:
                        screen_shake = 5
                        create_particle(578, 578+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                        mixer.music.set_volume(0.1)
                        mixer.music.play()
                if event.key == pygame.K_c: #3
                    try:
                        tile = c3[0]
                        x, y = tile.getpos()
                        if y >= 510 and y <= 725:
                        # if 1:
                            tile_group.remove(tile)
                            c3.remove(tile)
                            tile.v(False)
                            #screen_shake = default_shake
                            create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                            #mixer.music.play()
                        else:
                            screen_shake = 5
                            create_particle(659, 659+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                            mixer.music.set_volume(0.1)
                            mixer.music.play()
                    except:
                        screen_shake = 5
                        create_particle(659, 659+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                        mixer.music.set_volume(0.1)
                        #mixer.music.play()
                if event.key == pygame.K_v: #4
                    try:
                        tile = c4[0]
                        x, y = tile.getpos()
                        if y >= 510 and y <= 725:
                        # if 1:
                            tile_group.remove(tile)
                            c4.remove(tile)
                            tile.v(False)
                            #screen_shake = default_shake
                            create_particle(x, x+50, y+71, (84, 16, 148), 20, -2, 80, 20, 20, t=2)
                            #mixer.music.play()
                        else:
                            screen_shake = 5
                            create_particle(740, 740+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                            mixer.music.set_volume(0.1)
                            mixer.music.play()
                    except:
                        screen_shake = 5
                        create_particle(740, 740+50, 637, (255, 33, 122), 20, -2, 80, 20, 20, t=2)
                        mixer.music.set_volume(0.1)
                        mixer.music.play()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if songbeats[level][idx%len(songbeats[level])] == 1:
                    tile_group.append(Tile(random.randint(1,4)))
                idx += 1
            
        if screen_shake > 0:
            screen_shake -= 1

        render_offset = [0,0]
        if screen_shake:
            render_offset[0] = random.randint(0, 8) - 4
            render_offset[1] = random.randint(0, 8) - 4

        if screen_shake3 > 0:
            screen_shake3 -= 1

        render_offset3 = [0,0]
        if screen_shake3:
            render_offset3[0] = random.randint(0, 10) - 6
            render_offset3[1] = random.randint(0, 10) - 6

        if screen_shake4 > 0:
            screen_shake4 -= 1

        render_offset4 = [0,0]
        if screen_shake4:
            render_offset4[0] = random.randint(0, 10) - 6
            render_offset4[1] = random.randint(0, 10) - 6
        
        player.move(1)
        player2.move(2)
        linemaker.move(1)
        linemaker2.move(2)
        players.draw(he)
        players2.draw(hl)
        wn.blit(border, (475, 0))
        screen.blit(wn, render_offset)
        he.blit(hborder, (0, 0))
        hl.blit(hlborder, (825, 0))
        screen.blit(he, render_offset3)
        screen.blit(hl, render_offset4)
        pygame.display.update()
        mainclock.tick(120)
        #print(pygame.time.get_ticks())
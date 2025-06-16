import pygame
from sys import exit
import random

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Lospollosquantikos')
clock = pygame.time.Clock()

#---Text---
test_font = pygame.font.Font('graphics/RasterForgeRegular.ttf', 30)
text_font = pygame.font.Font('graphics/RasterForgeRegular.ttf', 50)
text_s = pygame.font.Font('graphics/RasterForgeRegular.ttf', 20)
no_c = pygame.image.load('graphics/no-c.png').convert_alpha()

#---BACKGROUND---
# Load and scale images
def load_scaled(path):
    return pygame.transform.scale(pygame.image.load(path), (800, 400))
bg = load_scaled('graphics/parallax-mountain-bg.png').convert_alpha()
mountains_far = load_scaled('graphics/parallax-mountain-montain-far.png').convert_alpha()
mountains_mid = load_scaled('graphics/parallax-mountain-mountains.png').convert_alpha()
trees_mid = load_scaled('graphics/parallax-mountain-trees.png').convert_alpha()
trees_fore = load_scaled('graphics/parallax-mountain-foreground-trees.png').convert_alpha()

text_surface = text_font.render('WELCOME', False, 'Black')
text_text = test_font.render('Next', False, 'Black')
x_surf = (text_surface.get_width())/2

#---LAB BACKGROUND ELEMENTS---
lab_desk = pygame.image.load('graphics/lab_desk.png').convert_alpha()
lab_desk1 = pygame.transform.scale(lab_desk, (900,165))
lab_cajon = pygame.image.load('graphics/lab_cajon.png').convert_alpha()
cajon = pygame.transform.scale(lab_cajon, (250,300))
lab_wall = load_scaled('graphics/lab_wall.png').convert_alpha()
clon_m = pygame.image.load('graphics/cloning_machine.png').convert_alpha()
clon_m = pygame.transform.scale_by(clon_m,12.0)
lab_wall1 = pygame.transform.scale_by(lab_wall,1.2)
bit_0 = pygame.image.load('graphics/cm_lside.png').convert_alpha()
bit_0 = pygame.transform.scale_by(bit_0,12.0)
bit_1 = pygame.image.load('graphics/cm_rside.png').convert_alpha()
bit_1 = pygame.transform.scale_by(bit_1,12.0)

def level1bg():
    """Draw level 1 background elements"""
    lab_desk1.set_colorkey('white')
    cajon.set_colorkey('white')
    screen.blit(lab_wall, (0, -10))
    screen.blit(lab_desk1, (-20, 245))
    screen.blit(cajon, (-20,0))
    screen.blit(cajon, (570,0))

def cmachine():
    """Draw cloning machine"""
    x = clon_m.get_width()
    x = x/2
    y = clon_m.get_height()
    clon_m.set_colorkey('white')
    screen.blit(clon_m,(410-x,450-y))

def button_cm():
    """Draw cloning machine buttons"""
    x = clon_m.get_width()
    x = x/2
    x_0 = bit_0.get_width()
    x_1 = bit_1.get_width()
    y = bit_0.get_height()
    bit_0.set_colorkey('white')
    bit_1.set_colorkey('white')
    screen.blit(bit_0,(400-x-x_0,450-y))
    screen.blit(bit_1,(400+x_1,425-y))

def button_pressed(x):
    """Handle button press to advance levels"""
    if sig_button0.draw():
        screen.fill('black')
        level1bg()
        x = x+1
    return x

# Background scrolling
scroll_speeds = [0.5, 0.06, 0.07, 0.08, 0.09]
positions = [0, 0, 0, 0, 0]

#---Main Character---
cat_sprites1 = [
    pygame.image.load('graphics/Cat/cat_sprite_1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/cat_sprite_2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/cat_sprite_3.png').convert_alpha()
]
cat_sprites_scaled = [
    pygame.transform.scale_by(cat_sprites1[0],4.0),
    pygame.transform.scale_by(cat_sprites1[1],4.0),
    pygame.transform.scale_by(cat_sprites1[2],4.0)
]

cat_sprites2 = [
    pygame.image.load('graphics/Cat/gato_sprite_2_0.png').convert_alpha(),
    pygame.image.load('graphics/Cat/gato_sprite_2_1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/gato_sprite_2_2.png').convert_alpha()
]

cat_rect = cat_sprites1[0].get_rect(topleft=(0, 300))

#---Side Characters---
browncat = [
    pygame.image.load('graphics/Cat/brown1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/brown2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/brown3.png').convert_alpha()
]
browndcat = [
    pygame.image.load('graphics/Cat/brownd1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/brownd2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/brownd3.png').convert_alpha()
]
brownacat = [
    pygame.image.load('graphics/Cat/browna1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/browna2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/browna3.png').convert_alpha()
]
orangecat = [
    pygame.image.load('graphics/Cat/orange1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/orange2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/orange3.png').convert_alpha()
]
orangecatw = [
    pygame.image.load('graphics/Cat/orangew1.png').convert_alpha(),
    pygame.image.load('graphics/Cat/orangew2.png').convert_alpha(),
    pygame.image.load('graphics/Cat/orangew3.png').convert_alpha()
]

brown = [
    pygame.transform.scale_by(browncat[0],4.0),
    pygame.transform.scale_by(browncat[1],4.0),
    pygame.transform.scale_by(browncat[2],4.0)
]
orange = [
    pygame.transform.scale_by(orangecat[0],4.0),
    pygame.transform.scale_by(orangecat[1],4.0),
    pygame.transform.scale_by(orangecat[2],4.0)
]

x = clon_m.get_width()
x = x/2
x_0 = (bit_0.get_width())/2

brown_x = (browncat[0].get_width())/2
x = x+x_0+brown_x
brown_y = browncat[0].get_height()

brown_x = 400-x
brown_y = brown_y-50

orange_rect = orangecat[0].get_rect(center=(400,-10))
orange_index = 0
orange_x = (orangecat[0].get_width())/2
x_1 = (bit_1.get_width())/2
orange_x = 400+x-x_1
orange_y = brown_y

cat_rect = cat_sprites1[0].get_rect(topleft=(0, 300))
cat_rect_scaled = cat_sprites_scaled[0].get_rect(topleft=(0, 300))
cat_index = 0
cat_index0 = 0
frame_count = 0
brown_rect = brown[0].get_rect(center=(400,-10))
brown_index = 0

# Machine elements
machine = pygame.image.load('graphics/US Robotics Palm Pilot.png').convert_alpha()
box = pygame.image.load('graphics/Box.png').convert_alpha()

# General Button class
class Button():
    def __init__(self, x, y, image, scale):  
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        
    def draw(self):
        """Draw button and handle click events"""
        action = False
        pos_user = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos_user):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action

# Level 1 back button
backi = pygame.image.load('graphics/backbutton.png').convert_alpha()
backi = pygame.transform.scale_by(backi,0.8)
backi.set_colorkey('white')
back = [
    backi.convert_alpha(),
    test_font.render('back', False, 'black')
]
back_1 = back[1].get_rect(topright=(772,20))
back_0 = back[0].get_rect(topright=(800,0))

# Next, start buttons  
nextb = pygame.image.load('graphics/next-button.png').convert_alpha()
next_button2 = Button(300,200,nextb,0.38)
next_button = Button(360,100,nextb,0.1)
startb = pygame.image.load('graphics/power-button.png').convert_alpha()
clickb = pygame.image.load('graphics/click.png').convert_alpha()
sigb = pygame.image.load('graphics/next-button.png').convert_alpha()
sigb.set_colorkey("Black")
sig_button0 = Button(390,280,sigb,0.1)
clone_b = Button(brown_x-35,brown_y+100,brown[0],1.0)
clone_o = Button(orange_x+35,orange_y+100,orange[0],1.0)
back_button = Button(back_0.x,back_0.y,back[0],1.0)

# Interdiction elements
inter = pygame.image.load('graphics/interdiction.png').convert_alpha()
keysb = pygame.image.load('graphics/keys.png').convert_alpha()

# Player movement
cat_pos = [500, 40]
player_speed = 5
cat_direction = "down"  # Initial direction

# Levels
nivel = 1
activ1 = False
activ2 = False
activ3 = False
gen = False
a = 0
textp1 = None
textp2 = None

# Main game loop
inicio = True

while inicio:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    if nivel == 1:
        # Background
        for i in range(len(positions)):
            positions[i] -= scroll_speeds[i]
            if positions[i] <= -800:
                positions[i] = 0

        for i, image in enumerate([bg, mountains_far, mountains_mid, trees_mid, trees_fore]):
            screen.blit(image, (positions[i], 0))
            screen.blit(image, (positions[i] + 800, 0))

        # Text
        screen.blit(text_surface, (400-x_surf, 50))

        # Animated cat
        frame_count += 1
        if frame_count % 10 == 0:  # Change sprite every 10 frames
            cat_index = (cat_index + 1) % 3

        cat_rect.x += 2  # Move right
        if cat_rect.left > 800:
            cat_rect.right = 0  # Reset position

        screen.blit(cat_sprites1[cat_index], cat_rect)

        if next_button.draw():
            nivel = 2  # CHANGE LEVEL

    elif nivel == 2:
        level1bg()
        inst1 = text_font.render('Level   ', False, 'White')
        inst2 = text_font.render('one', False, 'White')
        screen.blit(inst1, (100, 150))
        screen.blit(inst2, (320, 150))
        if next_button.draw():
            nivel = 3

    elif nivel == 3:
        level1bg()
        inst1 = test_font.render('In the macroscopic world', False, 'Black')
        inst2 = test_font.render('we can know all the', False, 'black')
        inst3 = test_font.render('properties of a system of', False, 'black')
        inst4 = test_font.render('particles', False, 'black')
        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        x_3 = (inst3.get_width())/2
        x_4 = (inst4.get_width())/2
        screen.blit(inst1, (400-x_1,100))
        screen.blit(inst2, (400-x_2,150))
        screen.blit(inst3, (400-x_3,200))
        screen.blit(inst4, (400-x_4,250))

        nivel = button_pressed(nivel)

    elif nivel == 4:
        inst1 = test_font.render('at the same time', False, 'black')
        inst2 = test_font.render('such as speed', False, 'Black')
        inst3 = test_font.render('or position', False, 'black')
        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        x_3 = (inst3.get_width())/2
        screen.blit(inst1, (400-x_1,100))
        screen.blit(inst2, (400-x_2,150))
        screen.blit(inst3, (400-x_3,200))

        nivel = button_pressed(nivel)

    elif nivel == 5:
        inst1 = test_font.render('Thus allowing', False, 'Black')
        inst2 = test_font.render('CLONATION', False, 'black')
        inst2 = pygame.transform.scale_by(inst2, 2.7)
        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        screen.blit(inst1, (400-x_1,100))
        screen.blit(inst2, (400-x_2,150))

        nivel = button_pressed(nivel)

    elif nivel == 6:
        screen.blit(lab_wall1, (-70, -10))
        inst1 = test_font.render('This is pimpi\'s', False, 'Black')
        inst2 = test_font.render('cloning machine', False, 'black')
        y = 20

        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        screen.blit(inst1, (400-x_1,y))
        screen.blit(inst2, (400-x_2,y+50))
        cmachine()
        nivel = button_pressed(nivel)

    elif nivel == 7:
        screen.blit(lab_wall1, (-70, -10))
        inst1 = test_font.render('and this is pimpi', False, 'Black')
        inst2 = test_font.render('(He\'s a professional hacker)', False, 'black')
        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        y = 20
        screen.blit(inst1, (400-x_1,y))
        screen.blit(inst2, (400-x_2,y+50))
        cmachine()
        frame_count += 1
        if frame_count % 10 == 0:  # Change sprite every 10 frames
            cat_index0 = (cat_index0 + 1) % 3

        cat_rect_scaled.x += 2  # Move right
        if cat_rect_scaled.left > 800:
            cat_rect_scaled.right = 0  # Reset position

        screen.blit(cat_sprites_scaled[cat_index0], cat_rect_scaled)
        nivel = button_pressed(nivel)

    elif nivel == 8:
        screen.fill('black')
        screen.blit(lab_wall1, (-70, -10))
        inst1 = test_font.render('Here he can clone bits', False, 'Black')
        y = 20
        x_1 = (inst1.get_width())/2
        screen.blit(inst1, (400-x_1,y))
        cmachine()
        frame_count += 1
        if frame_count % 10 == 0:  # Change sprite every 10 frames
            cat_index0 = (cat_index0 + 1) % len(cat_sprites_scaled)

        cat_rect_scaled.x += 2  # Move right
        if cat_rect_scaled.left > 800:
            cat_rect_scaled.right = 0  # Reset position

        screen.blit(cat_sprites_scaled[cat_index0], cat_rect_scaled)
        nivel = button_pressed(nivel)

    elif nivel == 9:
        next_aux = Button(700,300,nextb,0.1)
        screen.blit(lab_wall1, (-70, -10))
        inst1 = test_font.render('Use the buttons below', False, 'black')
        inst2 = test_font.render('to clone a bit', False, 'black')
        inst3 = test_font.render('(click one cat)', False, 'black')
        x_1 = (inst1.get_width())/2
        x_2 = (inst2.get_width())/2
        x_3 = (inst3.get_width())/2
        screen.blit(inst1, (400-x_1,y))
        screen.blit(inst2, (400-x_2,y+50))
        screen.blit(inst3, (400-x_3,y+100))
        cmachine()
        button_cm()
        x = clon_m.get_width()
        x = x/2
        x_0 = (bit_0.get_width())/2
    
        brown_x = (brown[0].get_width())/2
        x = x+x_0+brown_x
        brown_y = brown[0].get_height()

        brown_x = 400-x
        brown_y = brown_y-50
        
        if clone_b.draw():  # Clone brown cat
            nivel = nivel+1
        
        if clone_o.draw():  # Clone orange cat
            nivel = nivel+2

        if next_aux.draw():  # Next button
            nivel = 12  # CHANGE LEVEL

    elif nivel == 10:
        screen.blit(lab_wall1, (-70, -10))
        cmachine()
        button_cm()
        
        frame_count += 1.0

        if frame_count % 10 == 0:  # Change sprite every 10 frames
            brown_index = (brown_index + 1) % len(brown)
            
        brown_rect.y += 1
        brown_recti = brown_rect.y-830
        if 800 > brown_rect.bottom > 200:
            brown_rect.bottom = 0
            brown_rect.y = 801

        screen.blit(brown[brown_index], brown_rect)
        screen.blit(brown[brown_index], (brown_rect.x-50,200+brown_recti))
        screen.blit(brown[brown_index], (brown_rect.x+50,200+brown_recti))
        back[0].set_colorkey('white')
        if back_button.draw():
            screen.fill('black')
            screen.blit(lab_wall1, (-70, -10))
            cmachine()
            button_cm()
            nivel = 9
        screen.blit(back[1],back_1)
    
    elif nivel == 11:
        screen.blit(lab_wall1, (-70, -10))
        cmachine()
        button_cm()
        
        frame_count += 1.0

        if frame_count % 10 == 0:  # Change sprite every 10 frames
            orange_index = (orange_index + 1) % len(orange)
            
        orange_rect.y += 1
        orange_recti = orange_rect.y-830
        if 800 > orange_rect.bottom > 200:
            orange_rect.bottom = 0
            orange_rect.y = 801

        screen.blit(orange[orange_index], orange_rect)
        screen.blit(orange[orange_index], (orange_rect.x-50,200+orange_recti))
        screen.blit(orange[orange_index], (orange_rect.x+50,200+orange_recti))
        back[0].set_colorkey('white')
        if back_button.draw():
            screen.fill('black')
            screen.blit(lab_wall1, (-70, -10))
            cmachine()
            button_cm()
            nivel = 9
        screen.blit(back[1],back_1)
        
#---LEVEL 1--- WELCOME **********************************
    elif nivel == 12:
        # Background
        for i in range(len(positions)):
            positions[i] -= scroll_speeds[i]
            if positions[i] <= -800:
                positions[i] = 0

        for i, image in enumerate([bg, mountains_far, mountains_mid, trees_mid, trees_fore]):
            screen.blit(image, (positions[i], 0))
            screen.blit(image, (positions[i] + 800, 0))

        # Text
        text2 = text_s.render('Life was too easy...', False, 'White')
        text3 = text_s.render('So he traveled to the quantum kingdom ', False, 'White')
        screen.blit(text2, (100, 150))
        screen.blit(text3, (100, 170))

        # Animated cat
        frame_count += 1
        if frame_count % 10 == 0:  # Change sprite every 10 frames
            cat_index = (cat_index + 1) % len(cat_sprites1)

        cat_rect.x += 2  # Move right
        if cat_rect.left > 800:
            cat_rect.right = 0  # Reset position

        screen.blit(cat_sprites1[cat_index], cat_rect)

        # Check if button was clicked
        if next_button.draw():
            nivel = 13  # CHANGE LEVEL

#---LEVEL 2 ---INTRO CHARACTER
    elif nivel == 13:
        screen.fill("black")
        text2 = text_s.render('Level two', False, 'White')
        screen.blit(text2, (100, 150))
        # Scale sprite
        sprite_actual = cat_sprites2[int(frame_count) // 10 % 3]  # Each sprite shows for 10 frames
        sprite_escalado = pygame.transform.scale(sprite_actual, (100, 100))
        screen.blit(sprite_escalado, (200, 200))  # Adjust position to stay centered
        frame_count += 1

        if next_button.draw():
            nivel = 14  # CHANGE LEVEL

#---LEVEL 3 ---TRANSITION
    elif nivel == 14:
        screen.fill("black")
        text2 = text_s.render('He could not find a job :( ', False, 'White')
        screen.blit(text2, (100, 150))
        # Scale sprite
        sprite_actual = cat_sprites2[int(frame_count) // 10 % 3]  # Each sprite shows for 10 frames
        sprite_escalado = pygame.transform.scale(sprite_actual, (100, 100))
        screen.blit(sprite_escalado, (200, 200))  # Adjust position to stay centered
        frame_count += 1

        if next_button.draw():
            nivel = 15  # CHANGE LEVEL

#---LEVEL 4 ---NO-CLONING THEOREM
    elif nivel == 15:
        next_button1 = Button(600,280,nextb,0.1)
        screen.fill("black")
        text2 = text_s.render('There was an obstacle', False, 'White')
        text3 = text_s.render('The no-cloning theorem ', False, 'White')
        text4 = text_s.render('Lets call a friend to understand it', False, 'White' )
        screen.blit(text2, (60, 100))
        screen.blit(text3, (60, 120))
        screen.blit(text4,(60,300))
        screen.blit(no_c,(60,150))
        # Scale sprite
        sprite_actual = cat_sprites2[int(frame_count) // 10 % 3]  # Each sprite shows for 10 frames
        sprite_escalado = pygame.transform.scale(sprite_actual, (100, 100))
        screen.blit(sprite_escalado, (500, 40))  # Adjust position to stay centered
        frame_count += 1
        if next_button1.draw():
            nivel = 16  # CHANGE LEVEL

#---LEVEL 5 ---NEW CATS
    elif nivel == 16:
        screen.fill("black")
        text2 = text_s.render('This guy is not a hacker, but a test subject', False, 'White')
        text3 = text_s.render('He can change his color', False, 'White')
        text4 = text_s.render('So he can be, brown, orange or a mix', False, 'White' )
        text5 = text_s.render('We also have a cloning machine', False, 'White' )
        screen.blit(text2, (60, 50))
        screen.blit(text3, (60, 70))
        screen.blit(text4,(60,90))
        screen.blit(text5,(60,200))
        # Scale sprites
        brownc = browncat[frame_count // 10 % 3]  # Each sprite shows for 10 frames
        browncescalado = pygame.transform.scale(brownc, (100, 100))
        screen.blit(browncescalado, (60, 110))  # Brown cat
        orangec = orangecat[frame_count // 10 % 3]  # Each sprite shows for 10 frames
        orangeescalado = pygame.transform.scale(orangec, (100, 100))
        screen.blit(orangeescalado, (130, 110))  # Orange cat

        machinescalada = pygame.transform.scale(machine,(100,100))
        screen.blit(machinescalada,(60,250))

        frame_count += 1
        if next_button1.draw():
            nivel = 17  # CHANGE LEVEL

#---LEVEL 6 ---CLONING
    elif nivel == 17:
        powerM = Button(110,120,startb,0.1)
        screen.fill("black")
        text2 = text_s.render('Cloning machine', False, 'White')
        text3 = text_s.render('press          to activate', False, 'White')
        screen.blit(text2, (60, 20))
        screen.blit(text3,(20,150))
        # Scale sprites
        brownc = browncat[frame_count // 10 % 3]  # Each sprite shows for 10 frames
        browncescalado = pygame.transform.scale(brownc, (100, 100))

        screen.blit(browncescalado, (350, 50))  # Cat to clone

        machinescalada = pygame.transform.scale(machine,(100,100))
        screen.blit(machinescalada,(350,150))
        frame_count += 1

        if powerM.draw():
            activ1 = True
        if activ1:
            screen.blit(browncescalado, (300, 240))
            screen.blit(browncescalado, (400, 240)) 

        if next_button1.draw():
            nivel = 18  # CHANGE LEVEL   
            
#---LEVEL 7 ---CLONING
    elif nivel == 18:
        powerM = Button(110,120,startb,0.1)
        screen.fill("black")
        text2 = text_s.render('Cloning machine', False, 'White')
        text3 = text_s.render('press          to activate', False, 'White')
        screen.blit(text2, (60, 20))
        screen.blit(text3,(20,150))
        # Scale sprites
        orangec = orangecat[frame_count // 10 % 3]  # Each sprite shows for 10 frames
        orangescalado = pygame.transform.scale(orangec, (100, 100))

        screen.blit(orangescalado, (350, 50))  # Cat to clone

        machinescalada = pygame.transform.scale(machine,(100,100))
        screen.blit(machinescalada,(350,150))
        frame_count += 1

        if powerM.draw():
            activ2 = True
        if activ2:
            screen.blit(orangescalado, (300, 240))
            screen.blit(orangescalado, (400, 240)) 
        if next_button1.draw():
            nivel = 19  # CHANGE LEVEL
            
#---LEVEL 8 ---HIDE IT
    elif nivel == 19:
        screen.fill("black")
        text2 = text_s.render('Hide the cat in the box', False, 'White')
        text3 = text_s.render('Use          ', False, 'White')
        screen.blit(text2, (60, 20))
        screen.blit(text3, (60, 60))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cat_pos[1] -= player_speed
            cat_direction = "up"
        elif keys[pygame.K_DOWN]: 
            cat_pos[1] += player_speed
            cat_direction = "down"
        elif keys[pygame.K_LEFT]:
            cat_pos[0] -= player_speed
            cat_direction = "left"
        elif keys[pygame.K_RIGHT]:
            cat_pos[0] += player_speed
            cat_direction = "right"

        # Select sprite based on direction
        if cat_direction == "up":
            sprite_actual = orangecatw[frame_count // 10 % 3]
        elif cat_direction == "down":
            sprite_actual = orangecat[frame_count // 10 % 3]
        elif cat_direction == "left":
            sprite_actual = brownacat[frame_count // 10 % 3]
        elif cat_direction == "right":
            sprite_actual = browndcat[frame_count // 10 % 3]

        sprite_escalado = pygame.transform.scale(sprite_actual, (100, 100))
        screen.blit(sprite_escalado, (cat_pos[0], cat_pos[1]))

        frame_count += 1
        boxesc = pygame.transform.scale(box, (150, 150))
        screen.blit(boxesc,(20,250))
        keysc = pygame.transform.scale(keysb, (50, 50))
        screen.blit(keysc,(120,40))
        if next_button1.draw():
            nivel = 20  # CHANGE LEVEL
            
#---LEVEL 9 ---CLONING
    elif nivel == 20:
        powerM = Button(110,120,startb,0.1)
        clickC = Button(160,40,clickb,0.1)
        screen.fill("black")
        text2 = text_s.render('Try a mixture', False, 'White')
        text3 = text_s.render('press          to generate a clon', False, 'White')
        text4 = text_s.render('press          to create a mixture', False, 'White')
        screen.blit(text2, (60, 20))
        screen.blit(text3,(20,150))
        screen.blit(text4, (60, 40))
        if clickC.draw():
            activ3 = True
            gen = False
        if activ3 == True and gen == False:
            a = round(random.random(),2)
            textp1 = text_s.render(str(a), False, 'White')
            textp2 = text_s.render(str(round(1 - a, 2)), False, 'White')
            gen = True

        if textp1 and textp2:
            screen.blit(textp1, (300, 220))
            screen.blit(textp2, (300, 240))
        textpb = text_s.render('% brown', False, 'White')
        textpo = text_s.render('% orange', False, 'White')
        screen.blit(textpb, (360, 220))
        screen.blit(textpo, (360, 240))

        textpim = text_s.render('Pimpi cannot know those %', False, 'White')
        screen.blit(textpim,(360,200))

        boxesc = pygame.transform.scale(box, (150, 150))
        screen.blit(boxesc,(160,200))

        interesc = pygame.transform.scale(inter, (150, 150))
        if powerM.draw():
            screen.blit(interesc,(160,200))
        if next_button1.draw():
            nivel = 21  # CHANGE LEVEL
            
#---LEVEL 10 ---FINAL MESSAGE
    elif nivel == 21:
        screen.fill("black")
        text2 = text_s.render('Pimpi is now unemployed', False, 'White')
        text3 = text_s.render('Like the creators', False, 'White')
        text4 = text_s.render('it is impossible to create a perfect copy', False, 'White')
        text5 = text_s.render('of an unknown quantum state', False, 'White')
        screen.blit(text2, (60, 20))
        screen.blit(text3, (60, 40))
        screen.blit(text4, (60, 60))
        screen.blit(text5, (60, 80))

        textexit = text_s.render('Press to exit', False, 'White')
        screen.blit(textexit, (300, 290))
        if next_button1.draw():
            inicio = False
            pygame.quit()
            exit()
            
    pygame.display.update()
    clock.tick(60)
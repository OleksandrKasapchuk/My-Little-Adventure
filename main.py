from pygame import*

moving_x=False
moving_y=False
class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, size_x, size_y, player_x, player_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.size_x, self.size_y = size_x, size_y 
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y)) 

class Player(sprite.Sprite): 
    def __init__(self, player_image, size_x, size_y, player_x, player_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.size_x, self.size_y = size_x, size_y 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.jumped = False
        self.vel_y = 0
        self.gravity =True
        for num in range(1, 9):
            img_right = image.load(f'main_hero_walk_right/main_hero_walk_right_{num}.png')
            img_right = transform.scale(img_right, (self.size_x, self.size_y))
            img_left = transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.direction = 0
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 1
        keys = key.get_pressed() 
        if keys[K_d] or keys[K_RIGHT]: 
            dx = 5
            self.counter += 1
            self.direction = 1
        elif keys[K_a] or keys[K_LEFT]:
            dx = -5
            self.counter += 1
            self.direction = -1
        if keys[K_SPACE] and self.jumped == False:
            self.vel_y = -12
            self.jumped=True
        if keys[K_LEFT] == False and keys[K_a] == False and keys[K_RIGHT] == False and keys[K_d] == False:
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        #gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y
        if self.rect.bottom > win_height:
            self.rect.bottom = win_height
            self.vel_y = 0
        dy = self.vel_y
        #check for collision
        for tile in world.tile_list:
            #check for collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size_x, self.size_y):
                if tile[1].colliderect(self.rect.x + dx, self.rect.bottom, self.size_x, self.size_y):
                    self.jumped=False
                else:
                    dx = 0
            #check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size_x, self.size_y):
                #check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                #check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.gravity = False
                    self.vel_y = 0
        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy
    
class Enemy(sprite.Sprite): 
    def __init__(self, player_image, size_x, size_y, player_x, player_y, player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image), (size_x, size_y)) 
        self.speed = player_speed 
        self.rect = self.image.get_rect() 
        self.rect.x = player_x 
        self.rect.y = player_y 
        self.size_x, self.size_y = size_x, size_y 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 9):
            img_left = image.load(f'smal_skeleton_walk_left/smal_skeleton_walk_left_{num}.png')
            img_left = transform.scale(img_left, (self.size_x, self.size_y))
            img_right = transform.flip(img_left, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.direction = 1
        self.move_counter = 0
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        walk_cooldown = 2
        self.rect.x += self.speed
        self.move_counter += 1
        self.counter += 1
        if abs(self.move_counter) > 50:
            self.speed *= -1
            self.direction *= -1
            self.move_counter *= -1
        if self.counter > walk_cooldown:
            self.counter = 0	
            self.index += 1
        if self.index >= len(self.images_right):
            self.index = 0
        if self.direction == 1:
            self.image = self.images_right[self.index]
        if self.direction == -1:
            self.image = self.images_left[self.index]
        
tile_size=50

def draw_grid():
    for line in range(0, 17):
        draw.line(window, (255, 255, 255), (0, line * tile_size), (win_width, line * tile_size))
    for line in range(0, 25):
        draw.line(window, (255, 255, 255), (line * tile_size, 0), (line * tile_size, win_height))

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        dirt_img1 = image.load('img_dirt1.png')
        dirt_img2 = image.load('img_dirt2.png')
        stone_img = image.load('img_stone.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = transform.scale(dirt_img1, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 2:
                    img = transform.scale(dirt_img2, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 3:
                    img = transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])

world_data = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 1, 0, 3, 3, 3, 0, 0, 0, 0, 0], 
[1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0], 
[2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2], 
[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 3, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], 
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 3, 1], 
[0, 0, 2, 2, 1, 3, 1, 1, 3, 3, 1, 3, 0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 2, 2, 3], 
[2, 2, 3, 2, 2, 2, 3, 3, 3, 2, 2, 3, 0, 4, 4, 4, 4, 4, 4, 3, 2, 2, 3, 2, 2], 
[3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2]
]

world = World(world_data)

#window
win_width = 1250 
win_height = 850
window = display.set_mode((win_width, win_height)) 
display.set_caption("Secrets Of The Dungeon")

#backgrounds
backgrounds = []
current_background = 0

background0 = transform.scale(image.load("BGs/screen 0.png"), (win_width, win_height)) 
backgrounds.append(background0)

background1 = transform.scale(image.load("BGs/screen_1.png"), (win_width, win_height)) 
backgrounds.append(background1)

background2 = transform.scale(image.load("BGs/screen_2.png"), (win_width, win_height)) 
backgrounds.append(background2)
background3 = transform.scale(image.load("BGs/screen_3.png"), (win_width, win_height)) 
backgrounds.append(background3)

play_buttons = []
play_orange_img = image.load("btn_play/play_orange.png")
play_buttons.append(play_orange_img)
play_purple_img = image.load("btn_play/play_purple.png")
play_buttons.append(play_purple_img)
#buttons
cd = 0
class Button():
    def __init__(self, btn_image, x, y, size_x, size_y):
        self.image = btn_image
        self.rect = self.image.get_rect()
        self.size_x, self.size_y = size_x, size_y 
        self.rect.x = x
        self.rect.y = y
        self.index = 0
        self.wait = 5
        self.clicked = False
        self.action = False
    def draw(self):
        global cd
        self.image = play_buttons[self.index]
        cd += 1
        if cd > self.wait:
            self.index += 1
            cd = 0
        if self.index > 1:
            self.index = 0
        window.blit(self.image, (self.rect.x, self.rect.y))

        #get mouse position
        pos = mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.action = True
                self.clicked = True
                
        if mouse.get_pressed()[0] == 0:
            self.clicked = False
#create buttons
start = False
game = True
play = False
finish = False
FPS = 60
clock = time.Clock() 
#music
'''
mixer.init()
mixer.music.load('Bmusic.ogg') 
mixer.music.play()
'''
#sprites
player = Player('main_hero_walk_right/main_hero_walk_right_1.png',75,100, 50, 500, 5)
enemy = Enemy('smal_skeleton_walk_left/smal_skeleton_walk_left_1.png',70, 95 ,100,210, 2)
btn_play = Button(play_orange_img , 350, 400, 90, 90)
#boxes
while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False
    if finish != True:
        if not start:
            window.blit(backgrounds[current_background], (0,0))
            btn_play.draw()
            if btn_play.clicked:
                start = True
                play = True
                current_background+=1
        if play:
            window.blit(backgrounds[current_background], (0, 0))
            player.update()
            enemy.update()
            world.draw()
            #draw_grid()
            enemy.reset()
            player.reset()
            
    display.update()
    clock.tick(FPS)

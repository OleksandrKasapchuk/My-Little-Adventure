from pygame import*

#player allow moving
move_u, move_d, move_r, move_l = True, True, True, True
#murder move
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
        walk_cooldown = 2
        keys = key.get_pressed() 
        if keys[K_a] or keys[K_LEFT]:
            self.rect.x -= self.speed 
            self.counter += 1
            self.direction = -1
        if keys[K_d] or keys[K_RIGHT]: 
            self.rect.x += self.speed 
            self.counter += 1
            self.direction = 1
        if keys[K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped=True
        if keys[K_SPACE] == False:
            self.jumped=False
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
        self.direction = 0
    def reset(self): 
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self, target):
        walk_cooldown = 2
        global moving_x, moving_y
        if abs(self.rect.x - target.rect.x) <= 300 and abs(self.rect.y - target.rect.y) <= 300:
            if self.rect.x != target.rect.x:
                moving_x = True
            if moving_x:
                if self.rect.x - target.rect.x <= 0:
                    self.rect.x += self.speed
                    self.counter += 1
                    self.direction = 1
                if self.rect.x - target.rect.x >= 0:
                    self.rect.x -= self.speed
                    self.counter += 1
                    self.direction = -1
            if target.rect.x == self.rect.x:
                moving_x = False
                self.counter = 0
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
    for line in range(0, 20):
        draw.line(window, (255, 255, 255), (0, line * tile_size), (win_width, line * tile_size))
    for line in range(0, 25):
        draw.line(window, (255, 255, 255), (line * tile_size, 0), (line * tile_size, win_height))
class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = image.load('img_dirt.png')
		grass_img = image.load('img_stone.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = transform.scale(grass_img, (tile_size, tile_size))
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
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 1, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1]
]

world = World(world_data)
#window
win_width = 1250 
win_height = 850
window = display.set_mode((win_width, win_height)) 
display.set_caption("My Little Adventure") 
#backgrounds
backgrounds = []
current_background = 0

background1 = transform.scale(image.load("screen 1.png"), (win_width, win_height)) 
backgrounds.append(background1)
'''
background2 = transform.scale(image.load("background2.jpg"), (win_width, win_height)) 
backgrounds.append(background2)
background3 = transform.scale(image.load("background3.jpg"), (win_width, win_height)) 
backgrounds.append(background3)
background4 = transform.scale(image.load("background4.jpg"), (win_width, win_height)) 
backgrounds.append(background4)
background5 = transform.scale(image.load("background5.jpg"), (win_width, win_height)) 
backgrounds.append(background5)
background6 = transform.scale(image.load("background6.jpg"), (win_width, win_height)) 
backgrounds.append(background6)
background7 = transform.scale(image.load("background7.jpg"), (win_width, win_height)) 
backgrounds.append(background7)
background8 = transform.scale(image.load("background8.jpg"), (win_width, win_height)) 
backgrounds.append(background8)
background9 = transform.scale(image.load("background9.jpg"), (win_width, win_height)) 
backgrounds.append(background9)
background10 = transform.scale(image.load("background10.jpg"), (win_width, win_height)) 
backgrounds.append(background10)
'''

game = True
play = True
finish = False
FPS = 60
clock = time.Clock() 
#music
mixer.init()
mixer.music.load('Bmusic.ogg') 
mixer.music.play()
#sprites
player = Player('main_hero_walk_right/main_hero_walk_right_1.png',100,140, 50, 500, 5)
enemy = Enemy('smal_skeleton_walk_left/smal_skeleton_walk_left_1.png',110, 140 ,625,485, 2)
#boxes
while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False
    if finish != True:
        if play:
            player.update()
            enemy.update(player)
            window.blit(backgrounds[current_background], (0, 0))
            world.draw()
            draw_grid()
            enemy.reset()
            player.reset()
            
    display.update()
    clock.tick(FPS)

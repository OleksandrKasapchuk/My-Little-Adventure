from pygame import*

#player allow moving
move_r=True
move_l=True
#jumping
gravity = 1
jump_height=20
y_velocity=jump_height
jumping=False
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

class Player(GameSprite): 
    def update(self): 
        global jumping, y_velocity, jump_height
        keys = key.get_pressed() 
        '''
        if keys[K_w] or keys[K_UP] and self.rect.y > 5 and move_u: 
            self.rect.y = self.rect.y-self.speed 
            moving_u = True 
        if keys[K_s] or keys[K_DOWN] and self.rect.y < win_height - 80 and move_d: 
            self.rect.y = self.rect.y+self.speed 
            moving_d = True'''
        if keys[K_a] or keys[K_LEFT] and self.rect.x > 2 and move_l:
            self.rect.x = self.rect.x-self.speed 
            #moving_l = True
        if keys[K_d] or keys[K_RIGHT] and self.rect.x < win_width - 60 and move_r: 
            self.rect.x = self.rect.x+self.speed 
            #moving_r = True
        if keys[K_SPACE]:
            jumping=True
        if jumping:
            self.rect.y -= y_velocity
            y_velocity -= gravity
            if y_velocity < -jump_height:
                jumping=False
                y_velocity=jump_height
            
class Enemy(GameSprite): 
    def update(self, target): 
        global moving_x, moving_y
        if abs(self.rect.x - target.rect.x) <= 300 and abs(self.rect.y - target.rect.y) <= 300:
            if self.rect.x != target.rect.x:
                moving_x = True
            '''if self.rect.y != target.rect.y:
                moving_y = True'''
            if moving_x:
                if self.rect.x - target.rect.x <= 0:
                    self.rect.x += self.speed
                if self.rect.x - target.rect.x >= 0:
                    self.rect.x -= self.speed
            '''if moving_y:
                if self.rect.y - target.rect.y <= 0:
                    self.rect.y += self.speed
                if self.rect.y - target.rect.y >= 0:
                    self.rect.y -= self.speed'''
            if target.rect.x == self.rect.x:
                moving_x = False
            '''if target.rect.y == self.rect.y:
                moving_y = False'''

#window
win_width = 1000 
win_height = 600
window = display.set_mode((win_width, win_height)) 
display.set_caption("My Little Adventure") 
#backgrounds
backgrounds = []
current_background = 0
background1 = transform.scale(image.load("background1.jpg"), (win_width, win_height)) 
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
player = Player('кольт.png',100,140, 50, 305, 5)
enemy = Enemy('кольт.png',100, 130 ,625,320, 2)
#boxes
boxes = []
box1 = GameSprite('box.png', 80, 80, 500, 370, 0)
boxes.append(box1)
while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False
    if finish != True:
        if play:
            player.update()
            enemy.update(player)
            window.blit(backgrounds[current_background], (0, 0))
            box1.reset()
            enemy.reset()
            player.reset()
    display.update()
    clock.tick(FPS)

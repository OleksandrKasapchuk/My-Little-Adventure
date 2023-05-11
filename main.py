from pygame import*

move_r=True
move_l=True

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
#window
win_width = 1000 
win_height = 600
window = display.set_mode((win_width, win_height)) 
display.set_caption("My Little Adventure") 
background = transform.scale(image.load("background1.jpg"), (win_width, win_height)) 


game = True
play = True
finish = False
FPS = 60
clock = time.Clock() 

#sprites
player = Player('кольт.png',100,140, 50, 305, 5)


while game: 
    for e in event.get(): 
        if e.type == QUIT: 
            game = False
    if finish != True:
        if play:
            player.update() 
            window.blit(background, (0, 0))
            player.reset()
    display.update()
    clock.tick(FPS)
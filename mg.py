import pygame as pg
pg.init()

lvl = [  
      "                            .",
      "                            .",
      "                            .",
      "                            .",
      "                            .",
      "      * * *                 .",
      "   --------------           .",
      "                     *      .",
      "                   -----    .",
      "                            .",
      "        ---------           .",
      "                            .",
      "                  -----     .",
      "                            .",
      "ggggggggggggggggggggggggggggg"]

lvl_width = len(lvl[0])*50
lvl_height = len(lvl)*50

W = 280
H = 720

mw = pg.display.set_mode((W,H))
pg.display.set_caption("My game:)")

bg = "background/bgr.png"
player = "background/walk_rsoldier_stand.png"
platform = "background/platform.png"
ground = "background/ground.png"
diamond = "background/diamond.png"

side = "right"
walk = False
jump = False
counter = 0
change_x = 0
change_y = 0

map_items = pg.sprite.Group()
heroes = pg.sprite.Group()
items = pg.sprite.Group()

class Settings(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, img):
        super().__init__()

        self.speed = speed
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = y
        self.rect.y = y

def reset(self):
    mw.blit(self.image, (self.rect.x, self.rect.y))

class Player(Settings):
    def update(self):
        global side, walk, jump, change_y, change_x
        self.gravitation()

       
        if keys[pg.K_a]:
            self.rect.x -= self.speed
            side = "left"
            walk = True
        if keys[pg.K_d]:
            self.rect.x += self.speed
            side = "right"  
            walk = True
        if keys[pg.K_SPACE]:
            jump = True

        block_list = pg.sprite.spritecollide(self, map_items, False)    
        for block in block_list:
            if change_x > 0:
                self.rect.right = block.rect.left
            elif change_x < 0:
                self.rect.left = block.rect.right
        
        self.rect.y += change_y


        block_list = pg.sprite.spritecollide(self, map_items, False)
        for block in block_list:
            if change_y > 0:
                self.rect.bottom = block.rect.top 
            elif change_y < 0:
                self.rect.top = block.rect.bottom 
            change_y = 0


    def gravitation(self):
        global change_y

        if change_y == 0:
            change_y = 1
        else:
            change_y += 0   



    def jump(self):
        global change_y

        self.rect.y +=8
        platform_list = pg.srpite.spritecollide(self, map_items, False)  
        self.rect.y +=8

        if len(platform_list) > 0 or self.rect.bottom >= H:
            change_y -= 16

class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)    
    
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_config(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+W/2, -t+H/2

    l = min(0,1)
    l = max(-(camera.width - W), 1)
    t = max(-(camera.height - H), 1)
    t = min(0, t)

    return pg.Rect(l, t, w, h)

def player_animation(counter):
    global side, walk, jump, player

    if side == "right":
        if walk == False and jump == False:
             player = "walk_r/soldier_stand.png"
        elif jump == True:
             player = "walk_r/soldier_jump.png"
        elif counter <=3:
              player = "walk_r/soldier_walk1.png"  
        elif counter <=6:
              player = "walk_r/soldier_walk2.png"   

        if counter > 6:
            return 1
        else:
            return counter + 1

    if side == "left":      
        if walk == False and jump == False:
             player = "walk_l/soldier_stand.png"
        elif jump == True:
             player = "walk_l/soldier_jump.png"
        elif counter <=3:
              player = "walk_l/soldier_walk1.png"  
        elif counter <=6:
              player = "walk_l/soldier_walk2.png"   

        if counter > 6:
            counter = 1
        else:
            counter +=1           

x = y = 0        
for i in lvl:
    for j in i:
        if j == "-":
            j1 = Settings(x, y, 50, 30, 0, platform)
            map_items.add(j1)

        if j == "g":
            j1 = Settings(x, y, 50, 50, 0, ground) 
            map_items.add(j1) 

        if j == "*":
            j1 = Settings(x, y, 50, 50, 0, diamond)  
            items.add(j1)

        x += 50
y += 50
x = 0
    
game = True

hero = Player(250, 630, 50, 70, 5, player)
heroes.add(hero)
camera = Camera(camera_config, lvl_width, lvl_height)

while game:
    for e in pg.event.get():
     if e.type == pg.QUIT:
        game = False
     if e.type == pg.KEYUP:
         walk = False
         jump = False   

    mw.blit(pg.image.load(bg), (W,H), (0,0))
    keys = pg.key.get_pressed()

    camera.update(hero)
    for i in map_items:
        mw.blit(i.image, camera.apply(i))

    for i in items:
        mw.blit(i.image, camera.apply(i)) 
        if pg.sprite.collide_rect(hero, i):
            items.remove()


    for i in heroes:
        mw.blit(i.image, camera.apply(i))

    hero.update() 


    counter = player_animation(counter)  
    hero.image = pg.transform.scale(pg.image.load(player), (hero.width, hero.height)) 

    pg.display.update()
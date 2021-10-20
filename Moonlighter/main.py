from pico2d import *
import random
class background:

    def __init__(self):
        self.image = load_image('background.png')
    def draw(self):
        self.image.draw(640,360)

class character:
    def __init__(self):
        self.image = load_image('character.png')
        self.attack = load_image('characterattack.png')
        self.weapon = load_image('characterweapon.png')

        self.x, self.y = 200,300
        self.frame = 0
        self.dir = 0
        self.m_check = True
        self.x_dir = 0
        self.y_dir = 0

    def update(self):

        self.frame = (self.frame + 1) % 9
        # self.frame1 =(self.frame1 + 1) % 9
        self.x += self.x_dir * 5
        self.y += self.y_dir * 5
    def attack(self):

        self.a_frame = (self.a_frame + 1) % 6
        self.w_frame = (self.w_frame + 1) % 6
        self.image.clip_draw(self.frame * 89, self.dir, 100, 100, self.x, self.y)

    def draw(self):

        self.image.clip_draw(self.frame * 89, self.dir, 100, 100, self.x, self.y)


    def handle_events(self):

        global running
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_KEYDOWN and event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    if self.m_check == True:
                        self.dir = 0
                        self.x_dir += 2
                        if self.x == 180:
                            self.m_check = False
                    elif self.m_check == False:
                        self.x = 180

                if event.key == SDLK_LEFT:
                    self.dir = 200
                    self.x_dir -= 2

                if event.key == SDLK_UP:
                    self.dir = 300
                    self.y_dir += 2
                if event.key == SDLK_DOWN:
                    self.dir = 100
                    self.y_dir -= 2
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    self.x_dir -= 2
                if event.key == SDLK_LEFT:
                    self.x_dir += 2
                if event.key == SDLK_UP:
                    self.y_dir -= 2
                if event.key == SDLK_DOWN:
                    self.y_dir += 2




class BossMonster:
    def __init__(self):
        self.image = load_image('Boss.png')
    def draw(self):
        self.image.draw(700, 400)

class Monster1:
    def __init__(self):
        self.image = load_image('Monster1.png')
        self.x, self.y = random.randint(250,600),random.randint(150,450)
        self.check = True

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):

        if self.check == True:
            if self.x >= 180:
                self.x -= 10
                if self.x <= 180: self.check = False
        if self.check == False:
            if self.x <= 800:
                self.x += 10
                if self.x >=600: self.check = True


open_canvas(1280,720)

back = background()

player = character()

plyerattack = character()

boss = BossMonster()

lowmonster = [Monster1() for i in range(3)]

running = True

while running:

    player.handle_events()

    player.update()
    for monsters in lowmonster:
        monsters.update()

    clear_canvas()
    back.draw()
    player.draw()
    # player.attack()




    boss.draw()

    for monsters in lowmonster:
        monsters.draw()

    delay(0.05)
    update_canvas()

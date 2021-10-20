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
        self.a_frame = 0
        self.w_frame = 0
        self.dir = 0
        self.m_check = True
        self.x_dir = 0
        self.y_dir = 0
        self.turn = 0

    def update(self):

        self.frame = (self.frame + 1) % 9
        self.a_frame = (self.a_frame + 1) % 6
        self.w_frame = (self.w_frame + 1) % 6
        self.x += self.x_dir * 5
        self.y += self.y_dir * 5

    def draw(self):
        if self.turn == 0:
            self.image.clip_draw(self.frame * 89, self.dir, 100, 100, self.x, self.y)
        elif self.turn == 1:
            self.attack.clip_draw(self.a_frame * 136, 0, 100, 100, self.x, self.y, 65, 100)
            self.weapon.clip_draw(self.w_frame * 136, 0, 100, 100, self.x, self.y, 65, 80)
        elif self.turn == 2:
            self.attack.clip_draw(self.a_frame * 136, 100, 100, 100, self.x, self.y, 65, 100)
            self.weapon.clip_draw(self.w_frame * 136, 100, 100, 100, self.x, self.y, 65, 80)
        elif self.turn == 3:
            self.attack.clip_draw(self.a_frame * 136, 200, 100, 100, self.x, self.y, 65, 100)
            self.weapon.clip_draw(self.w_frame * 136, 200, 100, 100, self.x, self.y, 65, 80)
        elif self.turn == 4:
            self.attack.clip_draw(self.a_frame * 136, 300, 100, 100, self.x, self.y, 65, 100)
            self.weapon.clip_draw(self.w_frame * 136, 300, 100, 100, self.x, self.y, 65, 80)

    # def attackdraw(self):
    #     self.attack.clip_draw(self.a_frame * 133, self.dir, 100, 100, self.x, self.y)
    #     self.a_frame(self.a_frame + 1) % 6
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
                    self.turn = 0
                if event.key == SDLK_UP:
                    self.dir = 300
                    self.y_dir += 2
                    self.turn = 0
                if event.key == SDLK_DOWN:
                    self.dir = 100
                    self.y_dir -= 2
                    self.turn = 0
                if event.key == SDLK_j:
                    if self.dir == 0:
                        self.turn = 1
                    elif self.dir == 100:
                        self.turn = 2
                    elif self.dir == 200:
                        self.turn = 3
                    elif self.dir == 300:
                        self.turn = 4


            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    self.x_dir -= 2
                    self.turn = 0
                if event.key == SDLK_LEFT:
                    self.x_dir += 2
                    self.turn = 0
                if event.key == SDLK_UP:
                    self.y_dir -= 2
                    self.turn = 0
                if event.key == SDLK_DOWN:
                    self.y_dir += 2
                    self.turn = 0
                if event.key == SDLK_j:
                    self.turn = 0

class BossMonster:
    def __init__(self):
        self.image = load_image('Boss.png')
        self.x, self.y = 800, 400
        self.check = True
    def draw(self):
        self.image.draw(self.x, self.y)
    def update(self):
        if self.check == True:
            if self.y >= 180:
                self.y -= 1
                if self.y <= 180: self.check = False
        if self.check == False:
            if self.y <= 700:
                self.y += 1
                if self.y >= 700: self.check = True

class Monster1:
    def __init__(self):
        self.image = load_image('Monster1.png')
        self.x, self.y = random.randint(250,900),random.randint(150,450)
        self.check = True

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):

        if self.check == True:
            if self.x >= 180:
                self.x -= 10
                if self.x <= 180: self.check = False
        if self.check == False:
            if self.x <= 1100:
                self.x += 10
                if self.x >= 1100: self.check = True


open_canvas(1280,720)
back = background()
player = character()
plyerattack = character()
boss = BossMonster()
lowmonster = [Monster1() for i in range(5)]
running = True

while running:

    player.handle_events()
    player.update()
    for monsters in lowmonster:
        monsters.update()
    boss.update()
    clear_canvas()
    back.draw()
    player.draw()
    # player.attack()
    boss.draw()


    for monsters in lowmonster:
        monsters.draw()

    delay(0.03)
    update_canvas()

import game_framework
from pico2d import *
import game_world
import random
import Arrow


PIXEL_PER_METER = ( 10/ 7 )
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14


class Golem:

    def __init__(self):
        self.x, self.y = random.randint(500, 1100),random.randint(200,600)
        self.image = load_image('Monster_right.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.HP = 100

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.dir == 1:
            self.x += RUN_SPEED_PPS
            if self.x >= 1100:
                self.x -= RUN_SPEED_PPS
                self.dir = 0
        if self.dir == 0:
            self.x -= RUN_SPEED_PPS
            if self.x <= 150:
                self.x += RUN_SPEED_PPS
                self.dir = 1

    def draw(self):
        self.image.clip_draw(int(self.frame) * 20, 0, 20, 30, self.x, self.y)
        # draw_rectangle(*self.get_bb())

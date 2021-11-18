import game_framework
from pico2d import *
import game_world
import random


# Boy Action Speed
TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9


class Boss:

    def __init__(self):
        self.x, self.y = 600,200
        self.image = load_image('Boss_sprite.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 9

    def draw(self):
        self.image.clip_draw(int(self.frame) * 262, 0, 262, 252, self.x, self.y)
        # draw_rectangle(*self.get_bb())

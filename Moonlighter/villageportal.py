import game_framework
from pico2d import *


class Portal:

    def __init__(self):
        self.x, self.y = 600, 500
        self.image = load_image('villagedoor.png')

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

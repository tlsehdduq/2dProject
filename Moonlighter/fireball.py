from pico2d import *
import game_world
from Monster import Golem
import server
import collision

PIXEL_PER_METER = (10/5)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 100.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Fireball:
    image = None

    def __init__(self, x=400, y=300, velocity=0):

        if Fireball.image == None:
            Fireball.image = load_image('bossfireball.png')

        self.x, self.y, self.velocity = x, y, velocity


    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        self.y -= self.velocity + RUN_SPEED_PPS

        if collision.collide(self,server.player):
            server.player.HP -= 20
            game_world.remove_object(self)



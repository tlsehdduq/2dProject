from pico2d import *
import game_world
from Monster import Golem
import server
import collision
PIXEL_PER_METER = (30.0 / 1.0)
RUN_SPEED_KMPH = 1.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)



class arrow:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 10):

        if arrow.image == None:
            arrow.image = load_image('Arrow_left.png')

        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        self.x += self.velocity + RUN_SPEED_PPS
        for golems in server.golem:
            if collision.collide(self,golems):
                game_world.remove_object(self)
                golems.HP -= 10
                print(golems.HP)
                break



        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)



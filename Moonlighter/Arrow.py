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

    def __init__(self, x=400, y=300, velocity=10):

        if arrow.image == None:
            arrow.image = load_image('Arrow_left.png')

        self.x, self.y, self.velocity = x, y, velocity
        self.bosshitsound = load_wav('bosshit.wav')
        self.bosshitsound.set_volume(32)

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        self.x += self.velocity + RUN_SPEED_PPS
        for golems in server.golem:
            if collision.collide(self, golems):
                game_world.remove_object(self)
                if(server.player.HP < 1000):
                    server.player.HP += 5
                golems.HP -= 40
                golems.x += 10
                print(golems.HP)
                break

        if collision.collide(self, server.boss):
            server.boss.HP -= 30
            server.boss.x += 10
            if (server.player.HP < 1000):
                server.player.HP += 5
            self.bosshitsound.play()
            game_world.remove_object(self)
            print(server.boss.HP)

        for fgolems in server.flyinggolem:
            if collision.collide(self, fgolems):
                game_world.remove_object(self)
                if (server.player.HP < 1000):
                    server.player.HP += 5
                fgolems.HP -= 20
                fgolems.x += 10
                print(fgolems.HP)

        if self.x >= server.player.x + 250:
            game_world.remove_object(self)

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

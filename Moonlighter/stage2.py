import random
import json
import os

import loading
import villagestate
from pico2d import *
import game_framework
import game_world
import server
import stage2
from collision import collide

from Arrow import arrow
from Moonlighter import Player
from background import Background
from Monster import Golem
from portal import Portal
from Monster2 import FlyingGolem
from BOSS import Boss
name = "stage2"

def enter():
    server.player = Player()
    server.background = Background()
    server.golem = Golem()
    server.flyinggolem = FlyingGolem()
    server.Door = Portal()
    server.Arrow = arrow()


    game_world.add_object(server.background, 0)
    game_world.add_object(server.player, 1)
    game_world.add_object(server.Door, 1)

    server.golem = [Golem() for i in range(2)]
    server.flyinggolem = [FlyingGolem() for i in range(5)]
    game_world.add_objects(server.golem, 1)
    game_world.add_objects(server.flyinggolem, 1)
def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if collide(server.player, server.Door):
        game_framework.change_state(loading)

    for enemy in server.golem:
        if collide(enemy, server.Arrow):
            game_world.remove_object(server.Arrow)
            enemy.HP -= 10
            if enemy.HP <= 0:
                server.golem.remove(enemy)
                game_world.remove_object(enemy)
            print(enemy.HP)

    # if server.player.HP <= 0:
        # game_framework.change_state(villagestate)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()



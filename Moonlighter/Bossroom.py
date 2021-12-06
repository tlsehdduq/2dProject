import random
import json
import os

from pico2d import *
from collision import collide
import server
import game_framework
import game_world
import villagestate
import loading
from Moonlighter import Player
from Bossbackground import BossBackground
from BOSS import Boss
from Arrow import arrow


name = "Bossroom"



def enter():
    server.boss = Boss()
    server.player = Player()
    server.background = BossBackground()
    server.p_arrow = arrow()

    game_world.add_object(server.background, 0)
    game_world.add_object(server.player, 1)
    game_world.add_object(server.boss, 1)



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
    if server.player.HP <= 0:
        game_framework.change_state(villagestate)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()



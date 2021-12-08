import random
import json
import os

from pico2d import *

import collision
import server
import game_framework
import game_world
import villagestate

from Moonlighter import Player
from Bossbackground import BossBackground
from BOSS import Boss
from Arrow import arrow
from portal import Portal
import lastloading


name = "Bossroom"



def enter():
    server.boss = Boss()
    server.player = Player()
    server.background = BossBackground()
    server.p_arrow = arrow()
    server.Door = Portal()

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

    if collision.collide(server.boss,server.p_arrow):
        server.boss.HP -= 20
        print(server.boss.HP)

    if server.boss.HP <= 0:
        game_world.add_object(server.Door, 1)
        if collision.collide(server.player,server.Door):
            game_framework.change_state(lastloading)



def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()



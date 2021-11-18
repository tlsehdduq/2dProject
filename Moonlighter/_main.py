import random
import json
import os

import loading
import villagestate
from pico2d import *
import game_framework
import game_world

from Arrow import arrow
from Moonlighter import Player
from background import Background
from Monster import Golem
from portal import Portal

name = "_main"
player = None
background = None
golem = None
Door = None
p_arrow = None


def enter():
    global player
    global background
    global golem
    global Door
    global p_arrow
    player = Player()
    background = Background()
    golem = Golem()
    Door = Portal()
    p_arrow = arrow()

    game_world.add_object(background, 0)
    game_world.add_object(player, 1)
    game_world.add_object(Door, 1)

    golem = [Golem() for i in range(6)]

    game_world.add_objects(golem, 1)

    if player.fire_arrow():
        game_world.add_objects(p_arrow,1)



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
            player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    if collide(player, Door):
        game_framework.change_state(loading)
    for enemy in golem:
        if collide(player, enemy):
            print("COLLISION")
            player.HP -= 2
            print(player.HP)
    for golems in golem:
        if collide(golems, p_arrow):
            golems.HP -= 5
            print(golems.HP)
            if golems.HP <= 0:
                golem.remove(golems)
                game_world.remove_object(golems)

    if player.HP <= 0:
        game_framework.change_state(villagestate)
    for golems in golem:
        if golems.HP <= 0:
            game_world.remove_object(golems)


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

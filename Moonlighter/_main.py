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
    global Arrow
    player = Player()
    background = Background()
    golem = Golem()
    Door = Portal()
    Arrow = arrow()
    game_world.add_object(background, 0)
    game_world.add_object(player, 1)
    game_world.add_object(Door, 1)

    golem = [Golem() for i in range(6)]

    game_world.add_objects(golem, 1)


def fire_arrow(player):
    global Arrow
    Arrow = arrow(player.x, player.y, player.dir_x * 3)
    game_world.add_object(Arrow, 1)


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_j:
            fire_arrow(player)
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

        if collide(enemy,Arrow):
            golem.remove(enemy)
            game_world.remove_object(enemy)
            print('Collision')

    if player.HP <= 0:
        game_framework.change_state(villagestate)


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

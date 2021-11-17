import random
import json
import os

import loading

from pico2d import *
import game_framework
import game_world
import _main

from Moonlighter import Player
from village import Village
from villageportal import Portal

name = "villagestate"
player = None
background = None
Door = None



def enter():
    global player
    global background
    global Door
    player = Player()
    background = Village()
    Door = Portal()

    game_world.add_object(background, 0)
    game_world.add_object(player, 1)
    game_world.add_object(Door, 1)

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

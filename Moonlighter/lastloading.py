import random
import json
import os

from pico2d import *
import game_framework
import game_world
from loadingbackground import loadback
import villagestate

Loadback = None


name = "loading"

def enter():
    Loadback = loadback()
    game_world.add_object(Loadback, 0)


def exit():
    pass

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_state(villagestate)

def update():
    pass

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
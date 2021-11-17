import game_framework
from pico2d import *
import _main
import Moonlighter

from _main import Player

name = "TitleState"
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('title.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(_main)


def draw():
    clear_canvas()
    image.draw(640, 360)
    update_canvas()


def update():
    global logo_time

    if (logo_time > 1.0):
        logo_time = 0
        game_framework.change_state(_main)
    delay(0.01)
    logo_time += 0.01
    update_canvas()


def pause():
    pass


def resume():
    pass







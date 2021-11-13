import game_framework
from pico2d import *
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,

    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
}


class IdleState:
    def enter(Player, event):
        if event == RIGHT_DOWN:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 3
        elif event == LEFT_DOWN:
            Player.veloctiy -= RUN_SPEED_PPS
            Player.height = 2
        elif event == UP_DOWN:
            Player.veloctiy_y += RUN_SPEED_PPS
            Player.height = 0
        elif event == DOWN_DOWN:
            Player.veloctiy_y -= RUN_SPEED_PPS
            Player.height = 1

    def exit(Player, event):
        pass

    def do(Player):
        Player.frame = (Player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

    def draw(Player):
        if Player.velocity == 0 and Player.velocity_y == 0:
            Player.image.clip_draw(int(Player.frame) * 35, 35, 100, 100, Player.x, Player.y)
        else:
            Player.image.clip_draw(int(Player.frame) * 35, 35 * Player.height, 100, 100, Player.x, Player.y)


class Runstate:

    def enter(Player, event):
        if event == RIGHT_DOWN:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 3
        elif event == LEFT_DOWN:
            Player.velocity -= RUN_SPEED_PPS
            Player.height = 2
        elif event == UP_DOWN:
            Player.velocity_y += RUN_SPEED_PPS
            Player.height = 0
        elif event == DOWN_DOWN:
            Player.velocity_y -= RUN_SPEED_PPS
            Player.height = 1
        Player.dir = clamp(-1, Player.velocity, 1)

    def exit(Player, event):
        pass

    def do(Player):
        Player.frame = (Player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        Player.x += Player.velocity * game_framework.frame_time
        Player.x = clamp(25, Player.x, 500)

    def draw(Player):
        if Player.velocity == 0 and Player.velocity_y == 0:
            Player.image.clip_draw(int(Player.frame) * 35, 35, 100, 100, Player.x, Player.y)
        else:
            Player.image.clip_draw(int(Player.frame) * 35, 35 * Player.height, 100, 100, Player.x, Player.y)


class Player:
    def __init__(self):
        self.image = load_image('Player.png')
        self.x, self.y = 200, 300
        self.frame = 0
        self.dir = 1
        self.velocity = 0
        self.velocity_y = 0
        self.event_que = []
        self.cur_state = IdleState
        self.height = 0
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


next_state_table = {
    IdleState: {RIGHT_UP: Runstate, LEFT_UP: Runstate, UP_UP: Runstate, DOWN_UP: Runstate,
                RIGHT_DOWN: Runstate, LEFT_DOWN: Runstate, UP_DOWN: Runstate, DOWN_DOWN: Runstate},

    Runstate: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState,
               RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, UP_DOWN: IdleState, DOWN_DOWN: IdleState}
}

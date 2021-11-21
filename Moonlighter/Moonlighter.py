import game_framework
from pico2d import *
import game_world
from Arrow import arrow
import _main


PIXEL_PER_METER = (30.0 / 0.6)
RUN_SPEED_KMPH = 15.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, ATTACK_DOWN, = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,

    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,

    (SDL_KEYDOWN, SDLK_j): ATTACK_DOWN,


}


class IdleState:
    def enter(Player, event):
        if event == RIGHT_DOWN:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 0
        elif event == LEFT_DOWN:
            Player.velocity -= RUN_SPEED_PPS
            Player.height = 1
        elif event == UP_DOWN:
            Player.velocity_y += RUN_SPEED_PPS
            Player.UD = 0
            # Player.height = 3
        elif event == DOWN_DOWN:
            Player.velocity_y -= RUN_SPEED_PPS
            Player.UD = 1
            # Player.height = 3
        elif event == RIGHT_UP:
            Player.velocity -= RUN_SPEED_PPS
            Player.height = 0
        elif event == LEFT_UP:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 1
        elif event == UP_UP:
            Player.velocity_y -= RUN_SPEED_PPS
            Player.UD = 0
            # Player.height = 3
        elif event == DOWN_UP:
            Player.velocity_y += RUN_SPEED_PPS
            Player.UD = 1
            # Player.height = 3

    def exit(Player, event):

        if event == ATTACK_DOWN:
            Player.fire_arrow()

    def do(Player):
        Player.frame = (Player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Player.frame2 = (Player.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10

    def draw(Player):
        if Player.velocity == 0 and Player.velocity_y == 0:
            Player.image.clip_draw(int(Player.frame2) * 80, 100, 80, 100, Player.x, Player.y, 50, 50)
        elif Player.height == 0 or Player.height == 1:
            Player.RLimage.clip_draw(int(Player.frame) * 50, 59 * Player.height, 47, 59, Player.x, Player.y)
        elif Player.UD == 0 or Player.UD == 1:
            Player.UDimage.clip_draw(int(Player.frame3) * 50, 81 * Player.UD, 50, 81, Player.x, Player.y, 40, 40)


class Runstate:

    def enter(Player, event):
        if event == RIGHT_DOWN:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 0
        elif event == LEFT_DOWN:
            Player.velocity -= RUN_SPEED_PPS
            Player.height = 1
        elif event == UP_DOWN:
            Player.velocity_y += RUN_SPEED_PPS
            Player.UD = 0
            Player.height = 3
        elif event == DOWN_DOWN:
            Player.velocity_y -= RUN_SPEED_PPS
            Player.UD = 1
            Player.height = 3
        elif event == RIGHT_UP:
            Player.velocity -= RUN_SPEED_PPS
            Player.height = 0
        elif event == LEFT_UP:
            Player.velocity += RUN_SPEED_PPS
            Player.height = 1
        elif event == UP_UP:
            Player.velocity_y -= RUN_SPEED_PPS
            Player.UD = 0
            Player.height = 3
        elif event == DOWN_UP:
            Player.velocity_y += RUN_SPEED_PPS
            Player.UD = 1
            Player.height = 3

        Player.dir_x = int(Player.velocity)
        Player.dir_y = int(Player.velocity_y)

    def exit(Player, event):
        pass
        if event == ATTACK_DOWN:
            Player.fire_arrow()

    def do(Player):
        Player.frame = (Player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Player.frame2 = (Player.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        Player.frame3 = (Player.frame3 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Player.x += Player.velocity * game_framework.frame_time
        Player.y += Player.velocity_y * game_framework.frame_time
        Player.x = clamp(150, Player.x, 1100)
        Player.y = clamp(110, Player.y, 600)

    def draw(Player):
        if Player.velocity == 0 and Player.velocity_y == 0:
            Player.image.clip_draw(int(Player.frame2) * 80, 100, 80, 100, Player.x, Player.y, 50, 50)
        elif Player.height == 0 or Player.height == 1:
            Player.RLimage.clip_draw(int(Player.frame) * 50, 59 * Player.height, 47, 59, Player.x, Player.y)
        elif Player.UD == 0 or Player.UD == 1:
            Player.UDimage.clip_draw(int(Player.frame3) * 50, 81 * Player.UD, 50, 81, Player.x, Player.y, 40, 40)


class AttackState:
    def enter(Player, event):
        if event == ATTACK_DOWN:

            Player.Rat = 0

    def exit(Player, event):

        if event == ATTACK_DOWN:
            Player.fire_arrow()

    def do(Player):
        Player.frame = (Player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        Player.frame2 = (Player.frame2 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        Player.Ratframe = (Player.Ratframe + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

    def draw(Player):
        if Player.Rat == 0:
            Player.Rattack.clip_draw(int(Player.Ratframe) * 32, 0, 32, 34, Player.x, Player.y)


next_state_table = {
    IdleState: {RIGHT_UP: Runstate, LEFT_UP: Runstate, UP_UP: Runstate, DOWN_UP: Runstate,
                RIGHT_DOWN: Runstate, LEFT_DOWN: Runstate, UP_DOWN: Runstate, DOWN_DOWN: Runstate,
                ATTACK_DOWN: AttackState},

    Runstate: {RIGHT_UP: IdleState, LEFT_UP: IdleState, UP_UP: IdleState, DOWN_UP: IdleState,
               RIGHT_DOWN: IdleState, LEFT_DOWN: IdleState, UP_DOWN: IdleState, DOWN_DOWN: IdleState,
               ATTACK_DOWN: AttackState},

    AttackState: {RIGHT_UP: Runstate, LEFT_UP: Runstate, UP_UP: Runstate, DOWN_UP: Runstate,
                  RIGHT_DOWN: Runstate, LEFT_DOWN: Runstate, UP_DOWN: Runstate, DOWN_DOWN: Runstate,
                  ATTACK_DOWN: AttackState}

}


class Player:

    def __init__(self):
        self.image = load_image('Player1.png')
        self.RLimage = load_image('Left-down.png')
        self.UDimage = load_image('UP_down.png')
        self.Rattack = load_image('bowat_left_right.png')
        self.x, self.y = 200, 300
        self.frame2 = 0
        self.frame = 0
        self.frame3 = 0
        self.Ratframe = 0
        self.dir_x = 1
        self.dir_y = 1
        self.velocity = 0
        self.velocity_y = 0
        self.event_que = []
        self.cur_state = IdleState
        self.height = 0
        self.UD = 0
        self.Rat = 0
        self.cur_state.enter(self, None)
        self.HP = 1000

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def fire_arrow(self):
        Arrow = arrow(self.x, self.y, self.dir_x * 3)
        game_world.add_object(Arrow, 1)
        AttackState.draw()
    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

from pico2d import *

#character event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, DOWN_DOWN, UP_DOWN, DOWN_UP, UP_UP, ATTACK =range(9)

key_event_table = {
    (SDL_KEYDOWN,SDLK_w):UP_DOWN,
    (SDL_KEYDOWN,SDLK_s):DOWN_DOWN,
    (SDL_KEYDOWN, SDLK_a): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_d): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_w): UP_UP,
    (SDL_KEYUP, SDLK_s): DOWN_UP,
    (SDL_KEYUP, SDLK_a): LEFT_UP,
    (SDL_KEYUP, SDLK_d): RIGHT_UP,
    (SDL_KEYDOWN, SDLK_j): ATTACK
}


class character:
    def __init__(self):
        self.image = load_image('character.png')

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

        self.x, self.y = 200,300
        self.frame = 0
        self.a_frame = 0
        self.w_frame = 0
        self.dir = 0
        self.m_check = True
        self.x_dir = 0
        self.y_dir = 0
        self.turn = 0

    def change_state(self, state):
        # fill here
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.enter(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)


    def draw(self):
        self.cur_state.draw(self)
        # if self.turn == 0:
        #     self.image.clip_draw(self.frame * 89, self.dir, 100, 100, self.x, self.y, 80, 100)
        # elif self.turn == 1:
        #     self.attack.clip_draw(self.a_frame * 136, 0, 120, 100, self.x, self.y, 65, 100)
        #     self.weapon.clip_draw(self.w_frame * 136, 0, 120, 100, self.x, self.y, 65, 100)
        # elif self.turn == 2:
        #     self.attack.clip_draw(self.a_frame * 136, 100, 120, 100, self.x, self.y, 65, 100)
        #     self.weapon.clip_draw(self.w_frame * 136, 100, 120, 100, self.x, self.y, 65, 100)
        # elif self.turn == 3:
        #     self.attack.clip_draw(self.a_frame * 136, 200, 120, 100, self.x, self.y, 65, 100)
        #     self.weapon.clip_draw(self.w_frame * 136, 200, 120, 100, self.x, self.y, 65, 100)
        # elif self.turn == 4:
        #     self.attack.clip_draw(self.a_frame * 136, 300, 120, 100, self.x, self.y, 65, 100)
        #     self.weapon.clip_draw(self.w_frame * 136, 300, 120, 100, self.x, self.y, 65, 100)

    def handle_event(self,event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

class IdleState:
    def enter(character, event):
        if event == RIGHT_DOWN:
            character.x_dir += 2
            character.dir = 0
        elif event == LEFT_DOWN:
            character.x_dir -= 2
            character.dir = 200
        elif event == UP_DOWN:
            character.y_dir += 2
            character.dir = 300
        elif event == DOWN_DOWN:
            character.y_dir -= 2
            character.dir = 100

    def exit(character, event):
        pass

    def do(character):
        character.frame = (character.frame + 1) % 9
        character.x += character.x_dir * 5
        character.y += character.y_dir * 5
    def draw(character):
        if character.turn == 0:
            character.image.clip_draw(character.frame * 89, character.dir, 100, 100, character.x, character.y, 80, 100)

class RunState:
    def enter(character, event):
        if event == RIGHT_DOWN:
            character.x_dir += 2
            character.dir = 0
        elif event == LEFT_DOWN:
            character.x_dir -= 2
            character.dir = 200
        elif event == UP_DOWN:
            character.y_dir += 2
            character.dir = 300
        elif event == DOWN_DOWN:
            character.y_dir -= 2
            character.dir = 100
        elif event == RIGHT_UP:
            character.x_dir -= 2
            character.dir = 0
        elif event == LEFT_UP:
            character.x_dir += 2
            character.dir = 200
        elif event == UP_UP:
            character.y_dir -= 2
            character.dir = 300
        elif event == DOWN_UP:
            character.y_dir += 2
            character.dir = 100

    def exit(character,event):
        pass

    def do(character):
        character.frame = (character.frame + 1) % 9
        character.x += character.x_dir * 5
        character.y += character.y_dir * 5

    def draw(character):
        if character.turn == 0:
            character.image.clip_draw(character.frame * 89, character.dir, 100, 100, character.x, character.y, 80, 100)




next_state_table = {
    IdleState: {RIGHT_DOWN: RunState, RIGHT_UP: RunState,
                LEFT_DOWN: RunState, LEFT_UP: RunState,
                DOWN_DOWN: RunState, DOWN_UP: RunState,
                UP_DOWN: RunState, UP_UP: RunState},

    RunState: {RIGHT_DOWN: IdleState, RIGHT_UP: IdleState,
                LEFT_DOWN: IdleState, LEFT_UP: IdleState,
                DOWN_DOWN: IdleState, DOWN_UP: IdleState,
                UP_DOWN: IdleState, UP_UP: IdleState},
}
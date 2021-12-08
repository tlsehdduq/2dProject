import game_framework
from pico2d import *
import game_world
import random
import server
import collision
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

PIXEL_PER_METER = (10 / 0.3)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 9
FRAMES_PER_ACTION2 = 81


class Boss:

    def __init__(self):
        self.x, self.y = 600, 200
        self.image = load_image('Boss_sprite.png')
        self.deathimage = load_image('bossdeath.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.frame2 = 0
        self.HP = 1000
        self.speed = 0
        self.timer = 1.0
        self.wait_timer = 0
        self.build_behavior_tree()

        self.bossdeath = load_wav('bossdeath.wav')
        self.bossdeath.set_volume(100)


    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def update(self):
        self.bt.run()
        self.frame = (self.frame +
                      FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

        if self.HP <= 0:
            self.bossdeath.play()


        if collision.collide(self,server.player):
            server.player.HP -= 50
            print(server.player.HP)
        #
        # if collision.collide(self, server.p_arrow):
        #     self.HP -= 20
        #     self.hitsound.play()
        #     print(self.HP)

        # server.boss.remove(self)
        # game_world.remove_object(self)
        # game_framework.change_state(villagestate)

    def draw(self):
        if self.HP > 0:
            self.image.clip_draw(int(self.frame) * 262, 0, 262, 252, self.x, self.y)
        elif self.HP <= 0:
            self.deathimage.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def build_behavior_tree(self):
        wander_node = LeafNode("Wander", self.wander)
        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)
        chase_node = SequenceNode("Chase")
        chase_node.add_children(find_player_node, move_to_player_node)
        wander_chase_node = SelectorNode("WanderChase")
        wander_chase_node.add_children(chase_node, wander_node)
        self.bt = BehaviorTree(wander_chase_node)

        self.bt = BehaviorTree(chase_node)

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir = random.random() * 2 * math.pi
            print('Wander succes')
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 2.0
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def find_player(self):
        if self.HP > 0:
            distance = (server.player.x - self.x) ** 2 + (server.player.y - self.y) ** 2
            if distance < (PIXEL_PER_METER * 10) ** 2:
                return BehaviorTree.SUCCESS
            else:
                self.speed = 0
                return BehaviorTree.RUNNING
        elif self.HP <= 0:
            self.distance = 0

    def move_to_player(self):
        if self.HP > 0:
            self.speed = RUN_SPEED_PPS
            self.dir = math.atan2(server.player.y - self.y, server.player.x - self.x)
            return BehaviorTree.SUCCESS
        elif self.HP <= 0:
            self.speed = 0

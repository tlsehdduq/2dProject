import game_framework
from pico2d import *
import game_world
import random
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import server
import collision

PIXEL_PER_METER = (10 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6


class Golem:

    def __init__(self):
        self.x, self.y = random.randint(500, 1100), random.randint(200, 600)
        self.image = load_image('Monster_right.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.HP = 100
        self.speed = 0
        self.timer = 1.0
        self.wait_timer = 0
        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        self.bt.run()
        self.frame = (self.frame +
                      FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)


        if self.HP <= 0:
            server.golem.remove(self)
            game_world.remove_object(self)




    def draw(self):
        self.image.clip_draw(int(self.frame) * 20, 0, 20, 30, self.x, self.y)
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
        distance = (server.player.x - self.x) ** 2 + (server.player.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 10) ** 2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.RUNNING

    def move_to_player(self):
        self.speed = RUN_SPEED_PPS
        self.dir = math.atan2(server.player.y - self.y, server.player.x - self.x)
        return BehaviorTree.SUCCESS

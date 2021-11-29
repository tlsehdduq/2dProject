
level = 0
def indent():
    global level
    level += 1

def unindent():
    global level
    level -= 1

def print_indent():
    for i in range(level):
        print("    ", end='')


class BehaviorTree:
    FAIL, RUNNING, SUCCESS = -1, 0, 1

    def __init__(self, root_node):
        self.root = root_node

    def run(self):
        self.root.run()

    def print(self):
        self.root.print()


class Node: #최상위노드 두개의 함수만 가지고있고 노드밑에 차일드노드를 더하거나 여러개를 한ㄲ버ㅓㄴ에 더하는 함수
    def add_child(self, child):
        self.children.append(child)
    def add_children(self, *children):# 함수호출에 ㅣㅇㅆ어서 인자갯수가 달라지는 파이썬의 문법
        #인자들의 개수가 정해지지 않아도 ok *
        for child in children:
            self.children.append(child)


class SelectorNode(Node):
    #하위노드들이 한개라도 성공하면 성공
    #Node의 자식 클래스
    def __init__(self, name):
        self.children = []
        self.name = name
        self.prev_running_pos = 0 #prev_running_pos 앞선 실행에서 RUNNING으로 리턴한 자식노드위치를 지정


    def run(self):
        for pos in range(self.prev_running_pos, len(self.children)):
            result = self.children[pos].run()
            if BehaviorTree.RUNNING == result:
                self.prev_running_pos = pos
                return BehaviorTree.RUNNING
            elif BehaviorTree.SUCCESS == result:
                self.prev_running_pos = 0
                return BehaviorTree.SUCCESS
        self.prev_running_pos = 0
        return BehaviorTree.FAIL

    def print(self):
        print_indent()
        print("SELECTOR NODE: " + self.name)
        indent()
        for child in self.children:
            child.print()
        unindent()

class SequenceNode(Node): #Node의 차일드클래스
#하위노드들이 다성공해야 성공
    def __init__(self, name):
        self.children = []
        self.name = name
        self.prev_running_pos = 0

    def run(self):
        for pos in range(self.prev_running_pos, len(self.children)):
            result = self.children[pos].run()
            if BehaviorTree.RUNNING == result:
                self.prev_running_pos = pos
                return BehaviorTree.RUNNING
            elif BehaviorTree.FAIL == result:
                self.prev_running_pos = 0
                return BehaviorTree.FAIL
        self.prev_running_pos = 0
        return BehaviorTree.SUCCESS

    def print(self):
        print_indent()
        print("SEQUENCE NODE: " + self.name)
        indent()
        for child in self.children:
            child.print()
        unindent()


class LeafNode(Node):
    #테스크를 수행해야하기때무넹 인자로받고 이름과 함수로써 받는다.
    def __init__(self, name, func):
        self.name = name
        self.func = func

    def add_child(self, child):
        print("ERROR: you cannot add child node to leaf node")

    def add_children(self, *children):
        print("ERROR: you cannot add children node to leaf node")

    def run(self):#leaf노드와 연결된 함수를 실행
        return self.func()

    def print(self):
        print_indent()
        print("LEAF NODE: " + self.name)




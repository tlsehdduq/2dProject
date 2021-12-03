from pico2d import*

class state2Background:
    def __init__(self):
        self.image = load_image('background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

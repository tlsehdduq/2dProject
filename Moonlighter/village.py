from pico2d import*

class Village:
    def __init__(self):
        self.image = load_image('village.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

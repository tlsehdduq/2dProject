from pico2d import*

class loadback:
    def __init__(self):
        self.image = load_image('Load.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

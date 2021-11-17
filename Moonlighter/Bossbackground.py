from pico2d import*

class BossBackground:
    def __init__(self):
        self.image = load_image('BossRoom.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(620, 360)

from pico2d import*

class Village:
    def __init__(self):
        self.image = load_image('village.png')
        self.bgm = load_music('villagesound.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

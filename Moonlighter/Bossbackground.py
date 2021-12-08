from pico2d import*

class BossBackground:
    def __init__(self):
        self.image = load_image('BossRoom.png')
        self.bgm = load_music('dungeonback.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(620, 360)

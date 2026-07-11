from ursina import *
from core.colors import rgb


class GameSky:

    def __init__(self):

        self.sky = Sky(
            color=rgb(120,180,255)
        )
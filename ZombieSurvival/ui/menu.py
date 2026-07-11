from ursina import *
from core.colors import rgb


class MainMenu:

    def __init__(self, game):

        self.game = game


        self.root = Entity(
            parent=camera.ui
        )


        self.background = Entity(
            parent=self.root,
            model="quad",
            scale=(2,1),
            color=rgb(40,40,40)
        )


        self.title = Text(
            parent=self.root,
            text="ZOMBIE SURVIVAL",
            origin=(0,0),
            y=0.35,
            scale=2,
            color=color.white
        )


        self.play = Button(
            parent=self.root,
            text="ИГРАТЬ",
            y=0.05,
            scale=(0.35,0.1),
            color=color.lime
        )


        self.settings = Button(
            parent=self.root,
            text="НАСТРОЙКИ",
            y=-0.1,
            scale=(0.35,0.1),
            color=color.gray
        )


        self.exit = Button(
            parent=self.root,
            text="ВЫХОД",
            y=-0.25,
            scale=(0.35,0.1),
            color=color.red
        )


        self.play.on_click = self.game.start_world

        self.exit.on_click = application.quit



    def destroy(self):

        destroy(self.root)
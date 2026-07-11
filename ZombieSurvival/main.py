from ursina import *
from core.game import ZombieGame


app = Ursina(
    title="Zombie Survival",
    borderless=False
)


game = ZombieGame()


app.run()
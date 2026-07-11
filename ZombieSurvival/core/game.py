from ursina import *
from ursina.prefabs.sky import Sky

from ui.menu import MainMenu
from ui.hud import HUD
from ui.inventory import InventoryUI
from player.player import Player
from world.terrain import build_terrain, get_height_at
from world.foliage import scatter_rocks, scatter_buildings


class ZombieGame:

    def __init__(self):

        self.world_started = False

        self.menu = MainMenu(self)

    def start_world(self):

        if self.world_started:
            return

        self.world_started = True

        print("Создание мира...")

        # убрать меню
        self.menu.destroy()

        # небо
        Sky()

        # --- большая карта с холмами ---
        map_scale = 300
        height_scale = 22

        self.terrain, self.height_array, self.map_scale, self.height_scale = build_terrain(
            map_scale=map_scale,
            height_scale=height_scale,
        )

        # --- скалы и здания ---
        self.rocks = scatter_rocks(self.height_array, self.map_scale, self.height_scale, count=30)
        self.buildings = scatter_buildings(self.height_array, self.map_scale, self.height_scale, count=6)

        # --- HUD (голод/жажда/здоровье снизу слева) ---
        self.hud = HUD()

        # --- инвентарь (TAB) ---
        self.inventory = InventoryUI()

        # --- игрок ---
        spawn_y = get_height_at(self.height_array, 0, 0, self.map_scale, self.height_scale)
        self.player = Player(
            hud=self.hud,
            position=(0, spawn_y + 2, 0),
            speed=5,
        )
        self.player.set_inventory(self.inventory)

        print("Мир готов!")

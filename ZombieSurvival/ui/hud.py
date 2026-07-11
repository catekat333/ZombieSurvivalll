from ursina import *
from core.colors import rgb


class HUD(Entity):

    def __init__(self):
        super().__init__(parent=camera.ui)

        bg = rgb(0, 0, 0, 160)
        bar_w = 0.22
        bar_h = 0.025

        base_x = -0.82
        base_y = -0.44

        # --- Голод ---
        Text(
            parent=self,
            text="Голод",
            position=(base_x, base_y + 0.03),
            scale=0.6,
            color=color.white,
        )
        self.hunger_bg = Entity(
            parent=self,
            model="quad",
            color=bg,
            scale=(bar_w, bar_h),
            position=(base_x, base_y),
            origin=(-0.5, 0),
        )
        self.hunger_bar = Entity(
            parent=self.hunger_bg,
            model="quad",
            color=color.orange,
            scale=(1, 1),
            origin=(-0.5, 0),
            position=(-0.5, 0, -0.01),
        )

        # --- Жажда ---
        base_y2 = base_y - 0.05
        Text(
            parent=self,
            text="Жажда",
            position=(base_x, base_y2 + 0.03),
            scale=0.6,
            color=color.white,
        )
        self.thirst_bg = Entity(
            parent=self,
            model="quad",
            color=bg,
            scale=(bar_w, bar_h),
            position=(base_x, base_y2),
            origin=(-0.5, 0),
        )
        self.thirst_bar = Entity(
            parent=self.thirst_bg,
            model="quad",
            color=color.azure,
            scale=(1, 1),
            origin=(-0.5, 0),
            position=(-0.5, 0, -0.01),
        )

        # --- Здоровье (сверху над голодом/жаждой) ---
        base_y3 = base_y + 0.08
        Text(
            parent=self,
            text="Здоровье",
            position=(base_x, base_y3 + 0.03),
            scale=0.6,
            color=color.white,
        )
        self.health_bg = Entity(
            parent=self,
            model="quad",
            color=bg,
            scale=(bar_w, bar_h),
            position=(base_x, base_y3),
            origin=(-0.5, 0),
        )
        self.health_bar = Entity(
            parent=self.health_bg,
            model="quad",
            color=color.red,
            scale=(1, 1),
            origin=(-0.5, 0),
            position=(-0.5, 0, -0.01),
        )

    def update_bars(self, hunger, thirst, health=100):
        self.hunger_bar.scale_x = max(0.001, hunger / 100)
        self.thirst_bar.scale_x = max(0.001, thirst / 100)
        self.health_bar.scale_x = max(0.001, health / 100)

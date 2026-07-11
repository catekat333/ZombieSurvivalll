from ursina import *
from core.colors import rgb
from ursina.prefabs.first_person_controller import FirstPersonController


class Player(FirstPersonController):

    def __init__(self, hud=None, **kwargs):
        super().__init__(**kwargs)

        self.hud = hud
        self.inventory = None  # подключается снаружи (core/game.py), см. set_inventory()

        # характеристики выживания
        self.health = 100
        self.hunger = 100
        self.thirst = 100
        self._survival_timer = 0

        # "рука" игрока для удара — рисуется поверх камеры (в UI-слое)
        self.hand = Entity(
            parent=camera.ui,
            model="cube",
            texture="white_cube",
            color=rgb(205, 170, 140),
            scale=(0.14, 0.05, 0.05),
            position=(0.4, -0.32, 0),
            rotation=(0, 0, 0),
            origin=(-0.5, 0, 0),
        )

        self._punching = False

        if self.hud:
            self.hud.update_bars(self.hunger, self.thirst, self.health)

    def set_inventory(self, inventory_ui):
        self.inventory = inventory_ui

    def input(self, key):
        super().input(key)

        inventory_open = self.inventory and self.inventory.enabled

        if key == "left mouse down" and not self._punching and not inventory_open:
            self.punch()

        if key == "tab" and self.inventory:
            self.inventory.toggle()

    def punch(self):
        self._punching = True

        # взмах рукой вперёд-вбок и обратно
        self.hand.animate_position((0.15, -0.22, 0.15), duration=0.08, curve=curve.out_expo)
        self.hand.animate_rotation((10, -35, 0), duration=0.08, curve=curve.out_expo)

        invoke(self._punch_return, delay=0.09)

        # простая проверка попадания — луч из камеры вперёд
        hit_info = raycast(
            camera.world_position,
            camera.forward,
            distance=2.2,
            ignore=(self,),
        )
        if hit_info.hit and hasattr(hit_info.entity, "take_damage"):
            hit_info.entity.take_damage(15)

    def _punch_return(self):
        self.hand.animate_position((0.4, -0.32, 0), duration=0.12, curve=curve.out_expo)
        self.hand.animate_rotation((0, 0, 0), duration=0.12, curve=curve.out_expo)
        invoke(self._reset_punch, delay=0.12)

    def _reset_punch(self):
        self._punching = False

    def update(self):
        super().update()

        self._survival_timer += time.dt
        if self._survival_timer >= 1:
            self._survival_timer = 0
            self.hunger = max(0, self.hunger - 0.25)
            self.thirst = max(0, self.thirst - 0.35)

            if self.hunger <= 0 or self.thirst <= 0:
                self.health = max(0, self.health - 1)

            if self.hud:
                self.hud.update_bars(self.hunger, self.thirst, self.health)

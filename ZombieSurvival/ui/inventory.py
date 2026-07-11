from ursina import *
from core.colors import rgb


class InventoryUI(Entity):
    """
    Упрощённый инвентарь в духе Unturned: слева панель персонажа
    (тут просто заглушка), в центре сетка рюкзака, справа сетка
    предметов "поблизости". Открывается/закрывается по TAB.
    """

    def __init__(self):
        super().__init__(parent=camera.ui, enabled=False)

        panel_bg = rgb(20, 25, 20, 235)
        border = rgb(70, 100, 70, 255)
        slot_color = rgb(35, 45, 35, 255)
        slot_highlight = rgb(60, 90, 60, 255)
        nearby_slot_color = rgb(35, 30, 30, 255)
        nearby_slot_highlight = rgb(90, 60, 55, 255)

        # общая тёмная подложка на весь экран, чтобы клики не проходили в игру
        self.blocker = Entity(
            parent=self,
            model="quad",
            color=rgb(0, 0, 0, 120),
            scale=(3, 3),
            z=1,
        )

        # --- панель персонажа (слева) ---
        self.char_panel = Entity(
            parent=self,
            model="quad",
            color=panel_bg,
            scale=(0.34, 0.72),
            position=(-0.5, -0.03),
        )
        Text(
            parent=self.char_panel,
            text="Персонаж",
            position=(0, 0.33),
            origin=(0, 0),
            scale=1.3,
            color=color.white,
        )
        Entity(
            parent=self.char_panel,
            model="cube",
            color=rgb(90, 120, 80),
            scale=(0.12, 0.32, 0.08),
            position=(0, 0.02, -0.1),
        )

        # --- сетка рюкзака (центр) ---
        self.backpack_panel = Entity(
            parent=self,
            model="quad",
            color=panel_bg,
            scale=(0.5, 0.72),
            position=(-0.05, -0.03),
        )
        Text(
            parent=self.backpack_panel,
            text="Рюкзак",
            position=(0, 0.33),
            origin=(0, 0),
            scale=1.3,
            color=color.azure,
        )
        self.backpack_slots = self._make_grid(
            parent=self.backpack_panel,
            cols=5,
            rows=4,
            start=(-0.35, 0.23),
            gap=0.17,
            slot_scale=0.14,
            slot_color=slot_color,
            highlight=slot_highlight,
        )

        # --- сетка "поблизости" (справа) ---
        self.nearby_panel = Entity(
            parent=self,
            model="quad",
            color=panel_bg,
            scale=(0.34, 0.72),
            position=(0.42, -0.03),
        )
        Text(
            parent=self.nearby_panel,
            text="Поблизости",
            position=(0, 0.33),
            origin=(0, 0),
            scale=1.1,
            color=color.orange,
        )
        self.nearby_slots = self._make_grid(
            parent=self.nearby_panel,
            cols=3,
            rows=4,
            start=(-0.28, 0.23),
            gap=0.24,
            slot_scale=0.14,
            slot_color=nearby_slot_color,
            highlight=nearby_slot_highlight,
        )

    def _make_grid(self, parent, cols, rows, start, gap, slot_scale, slot_color, highlight):
        slots = []
        start_x, start_y = start
        for r in range(rows):
            for c in range(cols):
                slot = Button(
                    parent=parent,
                    model="quad",
                    color=slot_color,
                    highlight_color=highlight,
                    scale=slot_scale,
                    position=(start_x + c * gap, start_y - r * gap),
                )
                slots.append(slot)
        return slots

    def toggle(self):
        self.enabled = not self.enabled
        mouse.locked = not self.enabled
        mouse.visible = self.enabled

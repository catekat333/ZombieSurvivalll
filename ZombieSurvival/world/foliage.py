"""
Расстановка "декораций" по карте: скалы и здания-заготовки.
Пока без готовых 3D-моделей — скалы это неровные серые сферы,
здания это коробки с "дверью" (тёмная плашка), но всё стоит на
рельефе правильно и имеет коллайдер, во что уже можно врезаться /
на что можно залезть.
"""

import random
from ursina import Entity, color
from core.colors import rgb

from world.terrain import get_height_at


def scatter_rocks(height_array, map_scale, height_scale, count=35, min_dist_from_center=15):
    rocks = []
    half = map_scale / 2 * 0.9

    for _ in range(count):
        x = random.uniform(-half, half)
        z = random.uniform(-half, half)
        if (x ** 2 + z ** 2) ** 0.5 < min_dist_from_center:
            continue

        y = get_height_at(height_array, x, z, map_scale, height_scale)
        scale = random.uniform(1.2, 3.2)

        rock = Entity(
            model="cube",  # куб дешевле сферы и по рендеру, и по коллайдеру
            position=(x, y + scale * 0.25, z),
            scale=(scale, scale * random.uniform(0.5, 0.8), scale * random.uniform(0.8, 1.1)),
            rotation=(random.uniform(-15, 15), random.uniform(0, 360), random.uniform(-15, 15)),
            color=rgb(
                110 + random.randint(-15, 15),
                110 + random.randint(-15, 15),
                110 + random.randint(-15, 15),
            ),
            collider="box",
        )
        rocks.append(rock)

    return rocks


def scatter_buildings(height_array, map_scale, height_scale, count=8, min_dist_from_center=25):
    buildings = []
    half = map_scale / 2 * 0.8

    wall_colors = [
        rgb(150, 130, 100),
        rgb(120, 120, 130),
        rgb(140, 110, 90),
    ]

    for _ in range(count):
        x = random.uniform(-half, half)
        z = random.uniform(-half, half)
        if (x ** 2 + z ** 2) ** 0.5 < min_dist_from_center:
            continue

        y = get_height_at(height_array, x, z, map_scale, height_scale)

        width = random.uniform(6, 12)
        depth = random.uniform(6, 12)
        wall_height = random.uniform(4, 7)
        rot_y = random.choice([0, 90, 180, 270])

        walls = Entity(
            model="cube",
            position=(x, y + wall_height / 2, z),
            scale=(width, wall_height, depth),
            rotation=(0, rot_y, 0),
            color=random.choice(wall_colors),
            collider="box",
        )

        # дверь-плашка на одной из стен, чисто для вида
        door = Entity(
            parent=walls,
            model="cube",
            position=(0, -0.3, 0.501),
            scale=(0.18, 0.6, 0.02),
            color=rgb(35, 25, 20),
        )

        # плоская "крыша" — без коллайдера, чисто для вида (не нужно ходить по крышам)
        roof = Entity(
            model="cube",
            position=(x, y + wall_height + 0.15, z),
            scale=(width + 0.6, 0.3, depth + 0.6),
            rotation=(0, rot_y, 0),
            color=rgb(70, 55, 45),
        )

        buildings.append(walls)
        buildings.append(roof)

    return buildings

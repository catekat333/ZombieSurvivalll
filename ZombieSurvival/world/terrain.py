"""
Процедурная генерация рельефа для карты (в духе Unturned).

Оптимизации по сравнению с первой версией:
- heightmap меньше (65x65 вместо 129x129) -> в 4 раза меньше вершин
- визуальный меш и меш коллизии — РАЗНЫЕ: у визуального высокая детализация
  (skip=1), у коллизии — грубая (skip=4). Коллизия каждый кадр опрашивается
  игроком под ногами, и именно она чаще всего "съедает" FPS на больших
  ландшафтах, если использовать полную детализацию.
- текстура 'grass' не входит в комплект ursina -> без неё меш красится
  сплошным белым и ИГНОРИРУЕТ цвет. Используем встроенный 'white_cube',
  на который корректно ложится цвет (то есть трава просто одноцветная,
  без узора — но зато не лагает и не белая).
"""

import os
import numpy as np
from PIL import Image

from ursina import Terrain as UrsinaTerrain
from core.colors import rgb
from ursina import Entity, color


HEIGHTMAP_PATH = "assets/textures/heightmap.png"


def generate_heightmap(seed=None, size=65):
    """
    Строит height-массив (0..1) размера size x size и сохраняет как PNG,
    который потом скармливается ursina.Terrain.
    Возвращает (путь_к_файлу, height_array).
    """

    rng = np.random.default_rng(seed)

    x = np.linspace(0, 1, size)
    z = np.linspace(0, 1, size)
    xx, zz = np.meshgrid(x, z)

    height = np.zeros((size, size))

    layers = [
        (1.5, 1.0),
        (3.0, 0.5),
        (6.0, 0.2),
    ]

    for freq, amp in layers:
        phase_x = rng.uniform(0, 6.28318)
        phase_z = rng.uniform(0, 6.28318)
        height += amp * np.sin(xx * freq * np.pi * 2 + phase_x) * np.cos(zz * freq * np.pi * 2 + phase_z)

    # выравниваем центр карты (спавн игрока) — делаем плоским пятачком
    cx, cz = size // 2, size // 2
    radius = max(3, size // 10)
    yy, xx_idx = np.ogrid[:size, :size]
    dist = np.sqrt((xx_idx - cx) ** 2 + (yy - cz) ** 2)
    flatten_mask = np.clip(1 - dist / radius, 0, 1)
    height = height * (1 - flatten_mask) + height[cz, cx] * flatten_mask

    height -= height.min()
    if height.max() > 0:
        height /= height.max()

    os.makedirs(os.path.dirname(HEIGHTMAP_PATH), exist_ok=True)
    img = Image.fromarray((height * 255).astype(np.uint8), mode="L")
    img.save(HEIGHTMAP_PATH)

    return HEIGHTMAP_PATH, height


def get_height_at(height_array, world_x, world_z, map_scale, height_scale):
    """Высота рельефа в мировых координатах (x, z) -> world-space Y."""
    size = height_array.shape[0]
    u = (world_x / map_scale + 0.5) * (size - 1)
    v = (world_z / map_scale + 0.5) * (size - 1)
    u = int(min(max(u, 0), size - 1))
    v = int(min(max(v, 0), size - 1))
    return float(height_array[v][u]) * height_scale


def build_terrain(map_scale=300, height_scale=22, seed=None):
    """
    Создаёт на сцене ДВЕ сущности:
    - визуальную (детальная, без коллайдера — по ней просто едет камера)
    - коллизионную (грубая, невидимая, только для физики/ходьбы)
    Возвращает (visual_entity, height_array, map_scale, height_scale).
    """
    heightmap_path, height_array = generate_heightmap(seed=seed, size=65)
    heightmap_name = heightmap_path.rsplit(".", 1)[0]  # без расширения — так ждёт ursina.Terrain

    terrain_visual = Entity(
        model=UrsinaTerrain(heightmap_name, skip=1),
        scale=(map_scale, height_scale, map_scale),
        texture="white_cube",
        texture_scale=(60, 60),
        color=rgb(95, 140, 80),
    )

    # грубая копия того же рельефа — только для коллизии, не рендерится
    terrain_collision = Entity(
        model=UrsinaTerrain(heightmap_name, skip=4),
        scale=(map_scale, height_scale, map_scale),
        collider="mesh",
        visible=False,
    )

    # держим ссылку, чтобы Python не собрал объект как мусор
    terrain_visual.collision_mesh = terrain_collision

    return terrain_visual, height_array, map_scale, height_scale

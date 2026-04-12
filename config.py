import random

import pygame

import tool

# 按下偵測專區
is_pressing = []
for _ in range(20):
    is_pressing.append(False)


def reset_pressing():
    is_pressing[:] = [False] * len(is_pressing)


"""
dict[tuple[int, int], int]

{
    (0, 0): {"value": -1, "state": "covered"},
    (1, 0): {"value": 0, "state": "covered"},
    ...
}
"""


map = {}


def make_map(width, height):
    for y in range(height + 1):
        for x in range(width + 1):
            map[(x, y)] = {"value": random.randint(-1, 0), "state": "covered"}

    return width, height


def update_cell(game_map, x, y):
    if game_map[(x, y)]["value"] == -1:
        return
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (x + dx, y + dy) in game_map and game_map[(x + dx, y + dy)]["value"] == -1:
                count += 1
    game_map[(x, y)]["value"] = count

map_width, map_height = make_map(30, 20)

for x in range(map_width + 1):
    for y in range(map_height + 1):
        update_cell(map, x, y)


print(map)

a = 0

for k, v in map.items():
    c = v["value"]
    print(f"\033[{32 + c}m{k}\033[0m")
    if v["value"] == -1:
        a += 1
print(str(int(a / len(map) * 100)) + "%")

GRID_SIZE = 24
OFFSET_X = (1200 - (map_width * GRID_SIZE)) // 2
OFFSET_Y = (600 - (map_height * GRID_SIZE)) // 2


def draw_minesweeper_map(screen, game_map):
    for (x, y), cell in game_map.items():
        rect = pygame.Rect(
            OFFSET_X + x * GRID_SIZE,
            OFFSET_Y + y * GRID_SIZE,
            GRID_SIZE - 2,
            GRID_SIZE - 2,
        )
        if cell["state"] == "covered":
            pygame.draw.rect(
                screen,
                tool.Colors.two_color_change(tool.Colors.GRAY, tool.Colors.CYAN, (x + y) % 2 == 0),
                rect,
            )
        elif cell["state"] == "opened":
            pygame.draw.rect(screen, tool.Colors.WHITE, rect)
            if cell["value"] == -1:
                pygame.draw.circle(screen, tool.Colors.BLACK, rect.center, GRID_SIZE // 2)
            elif cell["value"] > 0:
                tool.show_text(
                    str(cell["value"]),
                    tool.Colors.BLUE,
                    rect.centerx,
                    rect.centery,
                    size=20,
                    screen_center=True,
                )

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

levels = [
    [10, 5, 40],  # map_width, map_height, GRING_SIZE
    [15, 7, 35],
    [20, 10, 35],
    [25, 15, 30],
    [25, 20, 25],
    [30, 20, 25],
    [30, 25, 20],
    [35, 25, 20],
    [40, 25, 18],
    [40, 30, 18],
]

color_map = {
    1: tool.Colors.BLUE,
    2: tool.Colors.GREEN,
    3: tool.Colors.ORANGE,
    4: tool.Colors.RED,
    5: tool.Colors.VIOLET,
    6: tool.Colors.PURPLE,
    7: tool.Colors.PINK,
    8: tool.Colors.BLACK
}


map = {}


def make_map(w, h, first_click_pos=None):
    bullet = 0
    for y in range(h):
        for x in range(w):
            if first_click_pos is not None and (x, y) == first_click_pos:
                is_bullet = False
            else:
                is_bullet = random.randint(1, 7) == 1  # 1/7 機率是地雷

            if is_bullet:
                map[(x, y)] = {"value": -1, "state": "covered"}
                bullet += 1
            else:
                map[(x, y)] = {"value": 0, "state": "covered"}

    return w, h, bullet


def update_cell(game_map, x, y):
    if game_map[(x, y)]["value"] == -1:
        return
    count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (x + dx, y + dy) in game_map and game_map[(x + dx, y + dy)]["value"] == -1:
                count += 1
    game_map[(x, y)]["value"] = count


map_width, map_height, map_bullets = 20, 20, 0


# print(map)

GRID_SIZE = 20
OFFSET_X = (1200 - (map_width * GRID_SIZE)) // 2
OFFSET_Y = (600 - (map_height * GRID_SIZE)) // 2

scroll_x = 0
scroll_y = 0

show_info = True

flags = 0


def draw_minesweeper_map(screen, game_map):
    for (x, y), cell in game_map.items():
        rect = pygame.Rect(
            OFFSET_X + scroll_x + x * GRID_SIZE,
            OFFSET_Y + scroll_y + y * GRID_SIZE,
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
                tool.show_text(str(cell["value"]), color_map[cell["value"]], rect.centerx, rect.centery, size=int(GRID_SIZE / 1.2), center=True)
        elif cell["state"] == "flagged":
            pygame.draw.rect(screen, tool.Colors.YELLOW, rect)
            tool.show_text("F", tool.Colors.RED, rect.centerx, rect.centery, size=int(GRID_SIZE / 1.2), center=True)


def reveal_empty(x, y):
    # 這裡要確保使用的是 config 裡面的 map
    if (x, y) not in map or map[(x, y)]["state"] != "covered":
        return

    map[(x, y)]["state"] = "opened"

    # 如果是空地 (0)，才繼續擴散
    if map[(x, y)]["value"] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                # 遞迴呼叫自己
                reveal_empty(x + dx, y + dy)


def check_win():
    for cell in map.values():
        # 如果有一格不是地雷 (value != -1)，但狀態還是覆蓋的 (covered)
        # 或者是插旗狀態 (flagged)，就代表還沒贏
        if cell["value"] != -1 and cell["state"] != "opened":
            return False
    # 如果全部的安全格子都開了，恭喜你贏了！
    return True


def reset_game():
    global flags, map, first_click
    flags = 0
    map = {}  # 先清空
    # 預先填滿格子，但 value 都是 0 (沒雷)，讓畫面上能畫出灰色方塊
    for y in range(map_height):
        for x in range(map_width):
            map[(x, y)] = {"value": 0, "state": "covered"}
    first_click = True


def first_click_reset(first_click_pos):
    global map, OFFSET_X, OFFSET_Y, map_width, map_height, map_bullets
    map_width, map_height, map_bullets = make_map(map_width, map_height, first_click_pos)
    for x, y in map.keys():
        update_cell(map, x, y)
    reveal_empty(*first_click_pos)

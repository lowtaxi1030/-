import pygame

import config
import tool

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("找地雷")
running, game_state = True, "menu"
clock = pygame.time.Clock()

# 按下偵測專區
is_pressing = []
for _ in range(20):
    is_pressing.append(False)


def reset_pressing():
    is_pressing[:] = [False] * len(is_pressing)


def get_current_mouse_state():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()


lv_button = draw_button = start_button = settings_button = upgrade_button = help_button = exit_button = player_rect = back_button = enemy_rect = pygame.Rect(0, 0, 0, 0)


while running:
    runed_time = pygame.time.get_ticks()
    screen_text = f"Escape Them! v1.0.0 - {game_state.replace('_', ' ')}"
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    mouse_pos, mouse_buttons = get_current_mouse_state()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
    # 主畫面
    if game_state == "menu":
        screen.fill(tool.Colors.YELLOW)
        tool.show_text("找地雷", tool.Colors.BLACK, 0, 80, size=50, screen_center=True)

        start_button = tool.text_button(
            "按我!" if start_button.collidepoint(mouse_pos) else "開始!",
            tool.Colors.two_color_change(tool.Colors.BLACK, tool.Colors.WHITE, start_button.collidepoint(mouse_pos)),
            tool.Colors.two_color_change(tool.Colors.GREEN, tool.Colors.DARK_GREEN, start_button.collidepoint(mouse_pos)),
            0,
            220,
            300,
            70,
            b_center=True,
        )
        # settings_button = tool.text_button(
        #     "設定",
        #     tool.Colors.two_color_change(tool.Colors.BLACK, tool.Colors.WHITE, settings_button.collidepoint(mouse_pos)),
        #     tool.Colors.two_color_change(tool.Colors.GREEN, tool.Colors.BLUE2, settings_button.collidepoint(mouse_pos)),
        #     WIDTH // 2 - 150,
        #     310,
        #     140,
        #     70,
        # )
        # upgrade_button = tool.text_button(
        #     "升級",
        #     tool.Colors.BLACK,
        #     tool.Colors.two_color_change(tool.Colors.ORANGE, tool.Colors.YELLOW, upgrade_button.collidepoint(mouse_pos)),
        #     WIDTH // 2 + 10,
        #     310,
        #     140,
        #     70,
        # )
        # help_button = tool.text_button(
        #     "幫助", tool.Colors.WHITE, tool.Colors.GRAY, 0, 400, 300, 70, b_center=True
        # )
        # 做好時再改成紫色
        exit_button = tool.text_button(
            "不要離開!!!" if exit_button.collidepoint(mouse_pos) else "離開",
            tool.Colors.WHITE,
            tool.Colors.two_color_change(tool.Colors.DARK_RED, tool.Colors.RED, exit_button.collidepoint(mouse_pos)),
            0,
            490,
            300,
            70,
            b_center=True,
        )
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # --- 第一階段：滑鼠按下 (DOWN) ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(mouse_pos):
                    is_pressing[0] = True
                # if settings_button.collidepoint(mouse_pos):
                #     is_pressing[1] = True
                # if upgrade_button.collidepoint(mouse_pos):
                #     is_pressing[2] = True
                # if exit_button.collidepoint(mouse_pos):
                #     is_pressing[3] = True

            # --- 第二階段：滑鼠放開 (UP) ---
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 只有當先前「有在按鈕內按下」且「現在也在按鈕內放開」才觸發
                if start_button.collidepoint(mouse_pos) and is_pressing[0]:
                    # reset_game()
                    game_state = "start"
                    # reset_scroll_ys()
                # if settings_button.collidepoint(mouse_pos) and is_pressing[1]:
                #     game_state = "setting_p1"
                # if upgrade_button.collidepoint(mouse_pos) and is_pressing[2]:
                #     game_state = "upgrade_hub"
                # if exit_button.collidepoint(mouse_pos) and is_pressing[3]:
                #     running = False
                reset_pressing()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_state = "setting_p1"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_state = "upgrade_p1"
    elif game_state == "start":
        screen.fill(tool.Colors.YELLOW)
        map_mouse_pos = ((mouse_pos[0] - config.OFFSET_X) // config.GRID_SIZE, (mouse_pos[1] - config.OFFSET_Y) // config.GRID_SIZE)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if map_mouse_pos in config.map:
                    config.map[map_mouse_pos]["state"] = "opened"
        config.draw_minesweeper_map(screen, config.map)

    pygame.display.flip()
    clock.tick(60)

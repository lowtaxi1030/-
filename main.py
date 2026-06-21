import sys

import pygame

import config
import tool

pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("找地雷")
running, game_state = True, "menu"
clock = pygame.time.Clock()

start_time = 0

total_paused_time = 0  # 總共暫停了多久（毫秒）
pause_start_time = 0  # 記錄按下暫停的那一刻系統時間
pause_game_time = 0

# 按下偵測專區
is_pressing = []
for _ in range(20):
    is_pressing.append(False)


def reset_pressing():
    is_pressing[:] = [False] * len(is_pressing)


def get_current_mouse_state():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()


lv_button = draw_button = start_button = settings_button = upgrade_button = help_button = exit_button = player_rect = back_button = (
    enemy_rect
) = pygame.Rect(0, 0, 0, 0)


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
                if exit_button.collidepoint(mouse_pos):
                    is_pressing[3] = True

            # --- 第二階段：滑鼠放開 (UP) ---
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # 只有當先前「有在按鈕內按下」且「現在也在按鈕內放開」才觸發
                if start_button.collidepoint(mouse_pos) and is_pressing[0]:
                    game_state = "level_select"
                    # reset_scroll_ys()
                # if settings_button.collidepoint(mouse_pos) and is_pressing[1]:
                #     game_state = "setting_p1"
                # if upgrade_button.collidepoint(mouse_pos) and is_pressing[2]:
                #     game_state = "upgrade_hub"
                if exit_button.collidepoint(mouse_pos) and is_pressing[3]:
                    running = False
                reset_pressing()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    running = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            game_state = "setting_p1"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            game_state = "upgrade_p1"
    # 關卡選擇
    elif game_state == "level_select":
        screen.fill(tool.Colors.YELLOW)
        draw_x, draw_y = 160, 150
        lv = 1
        for _ in range(2):
            for _ in range(5):
                lv_btn = tool.text_button(f"Lv.{lv}", tool.Colors.WHITE, tool.Colors.BLACK, draw_x, draw_y, 150, 60)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if lv_btn.collidepoint(event.pos):
                            lv_data = config.levels[lv - 1]
                            config.map_width = lv_data[0]
                            config.map_height = lv_data[1]
                            config.GRID_SIZE = lv_data[2]
                            config.reset_game()
                            config.OFFSET_X = (WIDTH - (config.map_width * config.GRID_SIZE)) // 2
                            config.OFFSET_Y = (HEIGHT - (config.map_height * config.GRID_SIZE)) // 2
                            game_state = "start"
                            select_level = lv
                draw_x += 180
                lv += 1
            draw_x = 160
            draw_y += 100

        tool.show_text("關卡選擇", tool.Colors.BLACK, 0, 50, size=50, screen_center=True)
    # 遊玩
    elif game_state == "start":
        screen.fill(tool.Colors.YELLOW)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            config.scroll_x -= 10
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            config.scroll_x += 10
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            config.scroll_y -= 10
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            config.scroll_y += 10

        full_map_w = config.map_width * config.GRID_SIZE
        full_map_h = config.map_height * config.GRID_SIZE

        buffer_x = config.GRID_SIZE * 5
        buffer_y = config.GRID_SIZE * 5

        # X 軸極限
        if full_map_w > WIDTH:
            limit_left = WIDTH - config.OFFSET_X - full_map_w - buffer_x
            limit_right = buffer_x - config.OFFSET_X
        else:
            limit_left = 0
            limit_right = 0

        # Y 軸極限
        if full_map_h > HEIGHT:
            limit_up = HEIGHT - config.OFFSET_Y - full_map_h - buffer_y
            limit_down = buffer_y - config.OFFSET_Y
        else:
            limit_up = 0
            limit_down = 0
        # ✨ 強大調試專區：只在第八關、且地圖大於視窗時 print 數據，免得洗版
        # if config.map_width == 35 and full_map_w > WIDTH:
        #     print(f"【X軸狀態】 實際GRID_SIZE: {config.GRID_SIZE}")
        #     print(f"  -> 限制器範圍 (下限 limit_left : 上限 limit_right) = ({limit_left} : {limit_right})")
        #     print(f"  -> 限制前的 scroll_x: {config.scroll_x} (你嘗試移動到的值)")
        #     print(f"  -> OFFSET_X 固定值: {config.OFFSET_X}")
        #     print(f"  -> 地圖左緣實時螢幕座標 (OFFSET + scroll): {config.OFFSET_X + config.scroll_x}")
        #     print("-" * 50)

        # 套用限制
        config.scroll_x = tool.num_range(limit_left, limit_right, config.scroll_x)
        config.scroll_y = tool.num_range(limit_up, limit_down, config.scroll_y)

        map_mouse_pos = (
            (mouse_pos[0] - (config.OFFSET_X + config.scroll_x)) // config.GRID_SIZE,
            (mouse_pos[1] - (config.OFFSET_Y + config.scroll_y)) // config.GRID_SIZE,
        )
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    mx, my = map_mouse_pos

                    # 2. 更新 GRID_SIZE
                    old_grid_size = config.GRID_SIZE
                    config.GRID_SIZE = tool.num_range(10, 100, config.GRID_SIZE + event.y * 2)
                    diff = config.GRID_SIZE - old_grid_size

                    full_map_w = config.map_width * config.GRID_SIZE
                    full_map_h = config.map_height * config.GRID_SIZE

                    # 3. 根據地圖大小決定補償策略
                    if full_map_w > WIDTH:
                        # 地圖大於螢幕：以滑鼠指著的地方為中心展開/收縮
                        config.scroll_x -= mx * diff
                    else:
                        # 地圖小於螢幕：強制 scroll 置零，並「即時動態更新 OFFSET_X」保持正中央！
                        config.scroll_x = 0
                        config.OFFSET_X = (WIDTH - full_map_w) // 2

                    if full_map_h > HEIGHT:
                        # 垂直方向同理
                        config.scroll_y -= my * diff
                    else:
                        config.scroll_y = 0
                        config.OFFSET_Y = (HEIGHT - full_map_h) // 2

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    config.reset_game()
                    game_state = "menu"
                if event.key == pygame.K_e:
                    config.show_info = not config.show_info
                if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                    pause_start_time = runed_time
                    game_state = "pause"

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_inside_map = 0 <= map_mouse_pos[0] < config.map_width and 0 <= map_mouse_pos[1] < config.map_height
                if is_inside_map:
                    if event.button == 1:
                        if config.first_click:  # 第一次點擊
                            config.first_click_reset(map_mouse_pos)
                            start_time = runed_time  # 記錄開始時間
                            total_paused_time = 0
                            config.first_click = False
                        if config.map[map_mouse_pos]["state"] == "flagged" or config.map[map_mouse_pos]["state"] == "opened":
                            pass  # 或是直接什麼都不寫，不進入後續判斷

                        # 如果沒插旗也沒開過，才開始處理踩雷或開地邏輯
                        else:
                            if config.map[map_mouse_pos]["value"] == -1:
                                # 踩到雷的邏輯
                                for _, cell in config.map.items():
                                    if cell["value"] == -1:
                                        cell["state"] = "opened"
                                config.draw_minesweeper_map(screen, config.map)
                                tool.show_text("Boom!", tool.Colors.RED, 0, 80, size=100, screen_center=True)
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                game_state = "game_over: Lose"

                            else:
                                # 沒踩到雷的邏輯（因為最外層已經擋掉 flagged，這裡絕對安全）
                                config.reveal_empty(*map_mouse_pos)
                                if config.check_win():
                                    config.draw_minesweeper_map(screen, config.map)
                                    tool.show_text("Clear!", tool.Colors.GREEN, 0, 80, size=100, screen_center=True)
                                    played_time = (runed_time - start_time) // 1000
                                    pygame.display.flip()
                                    pygame.time.wait(1000)
                                    game_state = "game_over: Win"
                    elif event.button == 3:
                        if config.map[map_mouse_pos]["state"] == "covered":
                            config.map[map_mouse_pos]["state"] = "flagged"
                            config.flags += 1
                        elif config.map[map_mouse_pos]["state"] == "flagged":
                            config.map[map_mouse_pos]["state"] = "covered"
                            config.flags -= 1
        config.draw_minesweeper_map(screen, config.map)
        if config.show_info:
            pygame.draw.rect(screen, tool.Colors.YELLOW, (35, 10, 180, 270), border_radius=10)
            tool.show_text(
                [
                    f"地雷數: {"?" if config.first_click else config.map_bullets}",
                    f"插旗數: {tool.num_range(0, None, config.flags)}",
                    f"剩餘地雷: {"?" if config.first_click else config.map_bullets - config.flags}",
                    "遊戲時間:",
                    (
                        f"{(pause_game_time := tool.show_time_min((runed_time - start_time - total_paused_time) // 1000))}"
                        if not config.first_click
                        else "0:00"
                    ),
                ],
                tool.Colors.BLACK,
                40,
                20,
                line_gap=10,
            )
            tool.show_text("按'E'可以開關我", tool.Colors.BLACK, 40, 230)
    elif game_state == "pause":
        """畫出上一貞的畫面並模糊，作為背景"""
        screen.fill(tool.Colors.YELLOW)
        config.draw_minesweeper_map(screen, config.map)
        if config.show_info:
            pygame.draw.rect(screen, tool.Colors.YELLOW, (35, 10, 180, 270), border_radius=10)
            tool.show_text(
                [
                    f"地雷數: {"?" if config.first_click else config.map_bullets}",
                    f"插旗數: {tool.num_range(0, None, config.flags)}",
                    f"剩餘地雷: {"?" if config.first_click else config.map_bullets - config.flags}",
                    "遊戲時間:",
                    f"{pause_game_time}" if not config.first_click else "0:00",
                ],
                tool.Colors.BLACK,
                40,
                20,
                line_gap=10,
            )
            tool.show_text("按'E'可以開關我", tool.Colors.BLACK, 40, 230)
        tool.screen_vague(20)
        """"""
        tool.show_text("暫停", tool.Colors.WHITE, 0, 50, size=40, screen_center=True)

        resume_button = tool.text_button("繼續", tool.Colors.WHITE, tool.Colors.BLUE, 0, 120, 200, 60, b_center=True)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # 計算這次暫停偷偷過了多久，並加到總暫停時間裡
                    total_paused_time += runed_time - pause_start_time
                    game_state = "start"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.collidepoint(mouse_pos):
                    total_paused_time += runed_time - pause_start_time
                    game_state = "start"
    # 結束
    elif game_state.startswith("game_over: "):
        screen.fill(tool.Colors.BLACK if game_state.endswith("Lose") else tool.Colors.GREEN)
        tool.show_text(
            ["遊戲結束!", f"Lv{select_level}"],
            tool.Colors.two_color_change(tool.Colors.RED, tool.Colors.WHITE, game_state.endswith("Lose")),
            0,
            50,
            size=50,
            screen_center=True,
        )
        tool.show_text(
            "你贏了!" if game_state.endswith("Win") else "炸裂了!",
            tool.Colors.two_color_change(tool.Colors.RED, tool.Colors.WHITE, game_state.endswith("Lose")),
            0,
            220,
            size=40,
            screen_center=True,
        )
        if game_state.endswith("Win"):
            tool.show_text(
                f"用時: {tool.show_time_min((runed_time - start_time - total_paused_time) // 1000)}",
                tool.Colors.WHITE,
                0,
                300,
                size=30,
                screen_center=True,
            )
        back_button = tool.text_button(
            "回到主選單",
            tool.Colors.WHITE,
            tool.Colors.two_color_change(
                tool.Colors.two_color_change(tool.Colors.RED, tool.Colors.DARK_RED, back_button.collidepoint(mouse_pos)),
                tool.Colors.two_color_change(tool.Colors.BLUE2, tool.Colors.BLUE, back_button.collidepoint(mouse_pos)),
                game_state.endswith("Lose"),
            ),
            0,
            370,
            300,
            70,
            b_center=True,
        )
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(mouse_pos):
                    is_pressing[0] = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if back_button.collidepoint(mouse_pos) and is_pressing[0]:
                    config.reset_game()
                    game_state = "menu"
                reset_pressing()

    pygame.display.flip()
    clock.tick(60)

sys.exit()

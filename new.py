import pygame
import sys
import random
import math

# =========================
#    DEATH SCREEN
# =========================
def death(screen):
    size = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.Font("Lexend-Regular.ttf", 50)
    small_font = pygame.font.Font("Lexend-Regular.ttf", 40)

    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (80, 60, 255), (size[0]/2 - 150, size[1]/2 - 150, 300, 300), border_radius=8)

        death_text = font.render("You Died", True, (255, 255, 255))
        screen.blit(death_text, death_text.get_rect(center=(size[0]/2, size[1]/2 - 90)))

        redo_button_1 = pygame.draw.rect(screen, (255, 100, 100), (size[0]/2 - 110, size[1]/2 - 30, 80, 40), border_radius=4)
        redo_button_2 = pygame.draw.rect(screen, (255, 100, 100), (size[0]/2 + 30, size[1]/2 - 30, 80, 40), border_radius=4)
        back_button = pygame.draw.rect(screen, (255, 180, 0), (size[0]/2 - 100, size[1]/2 + 40, 200, 60), border_radius=6)

        screen.blit(small_font.render("Redo", True, (0, 0, 0)), redo_button_1)
        screen.blit(small_font.render("Redo", True, (0, 0, 0)), redo_button_2)
        screen.blit(small_font.render("Level Select", True, (0, 0, 0)), back_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if redo_button_1.collidepoint(event.pos) or redo_button_2.collidepoint(event.pos):
                    return 0
                elif back_button.collidepoint(event.pos):
                    return 1

        pygame.display.flip()
        clock.tick(60)

# =========================
#    WIN SCREEN
# =========================
def win(screen):
    size = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.Font("Lexend-Regular.ttf", 50)
    small_font = pygame.font.Font("Lexend-Regular.ttf", 40)

    while True:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (60, 200, 60), (size[0]/2 - 150, size[1]/2 - 150, 300, 300), border_radius=8)

        win_text = font.render("You Dies", True, (255, 255, 255))
        screen.blit(win_text, win_text.get_rect(center=(size[0]/2, size[1]/2 - 90)))

        redo_button_1 = pygame.draw.rect(screen, (100, 255, 100), (size[0]/2 - 110, size[1]/2 - 30, 80, 40), border_radius=4)
        redo_button_2 = pygame.draw.rect(screen, (100, 255, 100), (size[0]/2 + 30, size[1]/2 - 30, 80, 40), border_radius=4)
        back_button = pygame.draw.rect(screen, (255, 180, 0), (size[0]/2 - 100, size[1]/2 + 40, 200, 60), border_radius=6)

        screen.blit(small_font.render("Redo", True, (0, 0, 0)), redo_button_1)
        screen.blit(small_font.render("Redo", True, (0, 0, 0)), redo_button_2)
        screen.blit(small_font.render("Level Select", True, (0, 0, 0)), back_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if redo_button_1.collidepoint(event.pos) or redo_button_2.collidepoint(event.pos):
                    return 0
                elif back_button.collidepoint(event.pos):
                    return 1

        pygame.display.flip()
        clock.tick(60)

# =========================
#    LEVEL SELECT SCREEN
# =========================
def circle(radius, label, color, coords, window, border_radius=4):
    label_font = pygame.font.Font("Lexend-Regular.ttf", 46)
    pygame.draw.circle(window, (0, 0, 0), coords, radius)
    pygame.draw.circle(window, color, coords, radius - border_radius)
    text_surface = label_font.render(label, True, (255, 255, 255))
    window.blit(text_surface, text_surface.get_rect(center=coords))
    return pygame.Rect(coords[0] - radius, coords[1] - radius, radius * 2, radius * 2)

def level_screen(window, unlocked_levels):
    clock = pygame.time.Clock()
    scroll_y = 0
    scroll_speed = 40

    circle_radius = 38
    spacing = 160
    margin_x = 100
    margin_y = 180
    levels_per_row = max(1, window.get_width() // spacing)

    bg_color = (249, 229, 56)
    level_color = (255, 153, 0)

    while True:
        window.fill(bg_color)

        level_rects = []
        total_levels = max(unlocked_levels, 0)
        total_rows = (total_levels + levels_per_row - 1) // levels_per_row
        max_scroll = max(0, total_rows * spacing + margin_y - window.get_height())

        for i in range(total_levels):
            row = i // levels_per_row
            col = i % levels_per_row
            x = margin_x + col * spacing
            y = margin_y + row * spacing - scroll_y
            rect = circle(circle_radius, str(i + 1), level_color, (x, y), window)
            level_rects.append((rect, i + 1))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for rect, level_id in level_rects:
                        if rect.collidepoint(event.pos):
                            return level_id
                elif event.button == 4:
                    scroll_y = max(scroll_y - scroll_speed, 0)
                elif event.button == 5:
                    scroll_y = min(scroll_y + scroll_speed, max_scroll)

        pygame.display.flip()
        clock.tick(60)

# =========================
#    GAME LOGIC
# =========================
pygame.init()
window = pygame.display.set_mode(flags=pygame.RESIZABLE)
window_size = window.get_size()
pygame.display.set_caption("RollRunner")
clock = pygame.time.Clock()

radius = 50
player_image_original = pygame.image.load("assets/skin1.png").convert_alpha()
player_image_original = pygame.transform.scale(player_image_original, (radius * 2, radius * 2))

types = {
    'normal': {
        'friction_range': (0.98, 0.995),
        'width_range': (100, 200),
        'height': 20,
        'image_path': 'assets/platform.png'
    }
}

def gen(level_id, num_platforms=30, start_x=200, start_y=500, challenge=0.5, challenge_variation=0.5):
    level = {}
    platforms = []
    x, y = start_x, start_y
    random.seed(level_id + 890)
    total_platforms = num_platforms + round(level_id * random.random())

    for idx in range(total_platforms):
        random.seed(level_id + idx + 890)
        type_data = types['normal']
        friction = random.uniform(*type_data['friction_range'])
        width = int(random.randint(*type_data['width_range']) / math.sqrt(challenge))
        height = type_data['height']
        image_path = type_data['image_path']
        platforms.append([x, y, width, height, image_path, friction])
        x += random.randint(200, 300) + width / 2 + random.uniform(challenge - challenge_variation, challenge + challenge_variation) * 100
        y += random.randint(-50, 50)

    level['end_x'], level['end_y'] = platforms[-1][0], platforms[-1][1]
    return platforms, level

def collide(plat, player_coords, radius, px, py, is_jumping, is_double_jumping, pr):
    x, y, w, h, _, friction = plat
    left_p, right_p = player_coords[0] - radius, player_coords[0] + radius
    top_p, bottom_p = player_coords[1] - radius, player_coords[1] + radius
    left_pl, right_pl = x, x + w
    top_pl, bottom_pl = y, y + h

    if right_p > left_pl and left_p < right_pl and bottom_p > top_pl and top_p < bottom_pl:
        if py > 0 and bottom_p - py <= top_pl:
            player_coords[1] = top_pl - radius
            py = 0
            is_jumping = is_double_jumping = False
            px *= friction
            pr = px
            if abs(px) < 0.1:
                px = pr = 0
        elif px > 0 and right_p <= left_pl + px:
            player_coords[0] = left_pl - radius
            px = pr = 0
        elif px < 0 and left_p >= right_pl + px:
            player_coords[0] = right_pl + radius
            px = pr = 0
    return player_coords, px, py, is_jumping, is_double_jumping, pr

def draw_platform(window, image, coords, cam_x, cam_y):
    window.blit(image, (coords[0] - cam_x, coords[1] - cam_y))

def create_rounded_tiled_surface(tile_img, width, height):
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    tw, th = tile_img.get_size()
    for x in range(0, width, tw):
        for y in range(0, height, th):
            surf.blit(tile_img, (x, y))
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=10)
    surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return surf

def run(level_id):
    level_data, level_info = gen(level_id)
    platform_tiles = [pygame.image.load(p[4]).convert_alpha() for p in level_data]
    platform_surfaces = [create_rounded_tiled_surface(platform_tiles[i], p[2], p[3]) for i, p in enumerate(level_data)]

    player_coords = [window_size[0] / 2, 0]
    px, py = 40, 0
    gravity, jump_speed = 0.5, -20
    is_jumping = is_double_jumping = False
    r = pr = 0
    bg_cam_y = 0

    btn_size, margin = 60, 20
    sw, sh = window_size
    buttons = {
        "left": pygame.Rect(sw - (btn_size * 3 + margin * 3), sh - (btn_size * 2 + margin * 2), btn_size, btn_size),
        "down": pygame.Rect(sw - (btn_size * 2 + margin * 2), sh - (btn_size + margin), btn_size, btn_size),
        "up": pygame.Rect(sw - (btn_size * 2 + margin * 2), sh - (btn_size * 3 + margin * 3), btn_size, btn_size),
        "right": pygame.Rect(sw - (btn_size + margin), sh - (btn_size * 2 + margin * 2), btn_size, btn_size),
    }

    def draw_arrow_button(surface, rect, direction):
        center = rect.center
        col = (0, 0, 0)
        if direction == "left":
            pts = [(center[0] + 15, center[1] - 20), (center[0] - 15, center[1]), (center[0] + 15, center[1] + 20)]
        elif direction == "right":
            pts = [(center[0] - 15, center[1] - 20), (center[0] + 15, center[1]), (center[0] - 15, center[1] + 20)]
        elif direction == "up":
            pts = [(center[0] - 20, center[1] + 15), (center[0], center[1] - 15), (center[0] + 20, center[1] + 15)]
        else:  # down
            pts = [(center[0] - 20, center[1] - 15), (center[0], center[1] + 15), (center[0] + 20, center[1] - 15)]
        pygame.draw.rect(surface, (200, 200, 200), rect, border_radius=12)
        pygame.draw.polygon(surface, col, pts)

    bg = pygame.image.load("assets/background.png").convert()
    bg = pygame.transform.scale(bg, (window_size[0] + 200, window_size[1] + 200))

    mouse_was_pressed = False
    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    px = -30
                elif ev.key == pygame.K_RIGHT:
                    px = 30
                elif ev.key == pygame.K_DOWN:
                    py = 50
                elif ev.key in (pygame.K_UP, pygame.K_SPACE):
                    if not is_jumping:
                        py, is_jumping = jump_speed, True
                    elif not is_double_jumping:
                        py, is_double_jumping = jump_speed, True

        if mouse_pressed[0] and not mouse_was_pressed:
            if buttons["left"].collidepoint(mouse_pos):
                px = -10
            if buttons["right"].collidepoint(mouse_pos):
                px = 10
            if buttons["down"].collidepoint(mouse_pos):
                py = 50
            if buttons["up"].collidepoint(mouse_pos):
                if not is_jumping:
                    py, is_jumping = jump_speed, True
                elif not is_double_jumping:
                    py, is_double_jumping = jump_speed, True
        mouse_was_pressed = mouse_pressed[0]

        py += gravity
        player_coords[1] += py
        player_coords[0] += px

        # Death check
        if player_coords[1] > window_size[1] + 1000:
            if death(window) == 1:
                return False
            player_coords = [window_size[0] / 2, 0]
            px = 4
            py = 0
            is_jumping = is_double_jumping = False
            r = pr = 0
            bg_cam_y = 0
            continue

        # Level complete
        if abs(player_coords[0] - level_info['end_x']) < 100 and abs(player_coords[1] - level_info['end_y']) < 100:
            # Show win screen
            result = win(window)
            if result == 1:  # Level select
                return False
            player_coords = [window_size[0] / 2, 0]
            px = 4
            py = 0
            is_jumping = is_double_jumping = False
            r = pr = 0
            bg_cam_y = 0
            continue

        cam_x = player_coords[0] - window_size[0] // 2
        cam_y = player_coords[1] - window_size[1] // 2
        bg_cam_y += (cam_y - bg_cam_y) * 0.05

        if is_jumping:
            pr *= 0.95
        r += pr

        window.blit(bg, (-100, -100 - bg_cam_y * 0.1))

        for i, plat in enumerate(level_data):
            draw_platform(window, platform_surfaces[i], plat[:2], cam_x, cam_y)
            player_coords, px, py, is_jumping, is_double_jumping, pr = collide(plat, player_coords, radius, px, py, is_jumping, is_double_jumping, pr)

        rot_img = pygame.transform.rotate(player_image_original, -r)
        rot_rect = rot_img.get_rect(center=(int(player_coords[0] - cam_x), int(player_coords[1] - cam_y)))
        window.blit(rot_img, rot_rect.topleft)

        for d, rect in buttons.items():
            draw_arrow_button(window, rect, d)

        pygame.display.flip()

# =========================
#    MAIN LOOP
# =========================
level = 1
if __name__ == "__main__":
    while True:
        selected_level = level_screen(window, level)
        if selected_level is None:
            break
        result = run(selected_level)
        if result is None:
            break
        if result is False:
            # Return to level select or exit
            continue
        if result is True:
            # Only unlock the next level if player completed the highest unlocked level
            if selected_level == level:
                level += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


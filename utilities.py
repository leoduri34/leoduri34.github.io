import random
import math
import sys
import pygame
from level_selector import level_screen as lvls
from death import death as ded
from death import win as winn
pygame.init()
window = pygame.display.set_mode(flags=pygame.RESIZABLE)
window_size = window.get_size()
pygame.display.set_caption("RollRunner")
clock = pygame.time.Clock()

radius = 50
player_image_original = pygame.image.load("assets/skin1.png").convert_alpha()
player_image_original = pygame.transform.scale(player_image_original, (radius * 2, radius * 2))

# Only one platform type now ─ static
types = {
    'normal': {
        'friction_range': (0.98, 0.995),
        'width_range': (100, 200),
        'height': 20,
        'image_path': 'assets/platform.png'
    }
}

def gen(level_id, num_platforms=30, start_x=200, start_y=500,
        challenge=0.5, challenge_variation=0.5):
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

        # Platform format: [x, y, w, h, image_path, friction]
        platforms.append([x, y, width, height, image_path, friction])

        x += random.randint(200, 300) + width / 2 + \
             random.uniform(challenge - challenge_variation,
                            challenge + challenge_variation) * 100
        y += random.randint(-50, 50)

    level['end_x'], level['end_y'] = platforms[-1][0], platforms[-1][1]
    return platforms, level

def collide(plat, player_coords, radius, px, py,
            is_jumping, is_double_jumping, pr):
    x, y, w, h, _, friction = plat
    left_p, right_p = player_coords[0] - radius, player_coords[0] + radius
    top_p, bottom_p = player_coords[1] - radius, player_coords[1] + radius
    left_pl, right_pl = x, x + w
    top_pl, bottom_pl = y, y + h

    if right_p > left_pl and left_p < right_pl \
       and bottom_p > top_pl and top_p < bottom_pl:
        if py > 0 and bottom_p <= top_pl + py:
            player_coords[1] = top_pl - radius
            py = 0
            is_jumping = False
            is_double_jumping = False
            px *= friction
            pr = px
            if abs(px) < 0.1:
                px = pr = 0
        elif px > 0 and right_p >= left_pl and left_p < left_pl:
            player_coords[0] = left_pl - radius
            px = pr = 0
        elif px < 0 and left_p <= right_pl and right_p > right_pl:
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
    pygame.draw.rect(mask, (255, 255, 255),
                     (0, 0, width, height), border_radius=10)
    surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return surf

def run(level_id):
    level_data, level_info = gen(level_id)
    platform_tiles = [pygame.image.load(p[4]).convert_alpha()
                      for p in level_data]
    platform_surfaces = [
        create_rounded_tiled_surface(platform_tiles[i], p[2], p[3])
        for i, p in enumerate(level_data)
    ]

    player_coords = [window_size[0] / 2, 0]
    px, py = 4, 0
    gravity, jump_speed = 0.3, -10
    is_jumping = is_double_jumping = False
    r = pr = 0
    bg_cam_y = 0

    btn_size, margin = 60, 20
    sw, sh = window_size
    buttons = {
        "left":  pygame.Rect(sw - (btn_size * 3 + margin * 3),
                             sh - (btn_size * 2 + margin * 2),
                             btn_size, btn_size),
        "down":  pygame.Rect(sw - (btn_size * 2 + margin * 2),
                             sh - (btn_size + margin),
                             btn_size, btn_size),
        "up":    pygame.Rect(sw - (btn_size * 2 + margin * 2),
                             sh - (btn_size * 3 + margin * 3),
                             btn_size, btn_size),
        "right": pygame.Rect(sw - (btn_size + margin),
                             sh - (btn_size * 2 + margin * 2),
                             btn_size, btn_size),
    }

    def draw_arrow_button(surface, rect, direction):
        center = rect.center
        col = (0, 0, 0)
        if direction == "left":
            pts = [(center[0] + 15, center[1] - 20),
                   (center[0] - 15, center[1]),
                   (center[0] + 15, center[1] + 20)]
        elif direction == "right":
            pts = [(center[0] - 15, center[1] - 20),
                   (center[0] + 15, center[1]),
                   (center[0] - 15, center[1] + 20)]
        elif direction == "up":
            pts = [(center[0] - 20, center[1] + 15),
                   (center[0], center[1] - 15),
                   (center[0] + 20, center[1] + 15)]
        else:  # down
            pts = [(center[0] - 20, center[1] - 15),
                   (center[0], center[1] + 15),
                   (center[0] + 20, center[1] - 15)]
        pygame.draw.rect(surface, (200, 200, 200), rect, border_radius=12)
        pygame.draw.polygon(surface, col, pts)

    bg = pygame.image.load("assets/background.png").convert()
    bg = pygame.transform.scale(bg, (window_size[0] + 200,
                                     window_size[1] + 200))

    mouse_was_pressed = False
    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT \
               or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_LEFT:
                    px = -10
                elif ev.key == pygame.K_RIGHT:
                    px = 10
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

        if player_coords[1] > window_size[1] + 1000:
            if ded(window) == 1:
                return False
            player_coords = [window_size[0] / 2, 0]
            px = 4
            py = 0
            is_jumping = is_double_jumping = False
            r = pr = 0
            bg_cam_y = 0
            continue

        if abs(player_coords[0] - level_info['end_x']) < 100 and \
           abs(player_coords[1] - level_info['end_y']) < 100:
            if winn(window) == 1:
                return True

        cam_x = player_coords[0] - window_size[0] // 2
        cam_y = player_coords[1] - window_size[1] // 2
        bg_cam_y += (cam_y - bg_cam_y) * 0.05

        if is_jumping:
            pr *= 0.95
        r += pr

        window.blit(bg, (-100, -100 - bg_cam_y * 0.1))

        for i, plat in enumerate(level_data):
            draw_platform(window, platform_surfaces[i], plat[:2], cam_x, cam_y)
            player_coords, px, py, is_jumping, is_double_jumping, pr = \
                collide(plat, player_coords, radius,
                        px, py, is_jumping, is_double_jumping, pr)

        rot_img = pygame.transform.rotate(player_image_original, -r)
        rot_rect = rot_img.get_rect(
            center=(int(player_coords[0] - cam_x),
                    int(player_coords[1] - cam_y)))
        window.blit(rot_img, rot_rect.topleft)

        for d, rect in buttons.items():
            draw_arrow_button(window, rect, d)

        pygame.display.flip()

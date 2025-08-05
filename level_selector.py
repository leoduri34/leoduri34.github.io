import pygame



def circle(radius, label, color, coords, window, border_radius=4):
    # Load Lexend font (make sure 'Lexend-Regular.ttf' is in your project folder)
    label_font = pygame.font.Font("Lexend-Regular.ttf", 46)

    # Draw black border circle (outer circle)
    pygame.draw.circle(window, (0, 0, 0), coords, radius)

    # Draw main colored circle (inner circle slightly smaller to show black border)
    pygame.draw.circle(window, color, coords, radius - border_radius)

    # Render and blit label
    text_surface = label_font.render(label, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=coords)
    window.blit(text_surface, text_rect)

    return pygame.Rect(coords[0] - radius, coords[1] - radius, radius * 2, radius * 2)


def level_screen(window, unlocked_levels):
    pygame.init()
    clock = pygame.time.Clock()
    scroll_y = 0
    scroll_speed = 40
    max_scroll = 0

    circle_radius = 38
    spacing = 160
    margin_x = 100
    margin_y = 180
    levels_per_row = max(1, window.get_width() // spacing)

    # High contrast orange/yellow scheme
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
                exit()
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

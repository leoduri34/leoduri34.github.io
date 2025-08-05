import pygame
import sys
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
def death(screen):
    size = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 40)

    while True:

        # Background panel
        pygame.draw.rect(screen, (80, 60, 255), (size[0]/2 - 150, size[1]/2 - 150, 300, 300), border_radius=8)

        # Text
        death_text = font.render("You Died", True, (255, 255, 255))
        screen.blit(death_text, death_text.get_rect(center=(size[0]/2, size[1]/2 - 90)))

        # Buttons
        redo_button_1 = pygame.draw.rect(screen, (255, 100, 100), (size[0]/2 - 110, size[1]/2 - 30, 80, 40), border_radius=4)
        redo_button_2 = pygame.draw.rect(screen, (255, 100, 100), (size[0]/2 + 30, size[1]/2 - 30, 80, 40), border_radius=4)
        back_button = pygame.draw.rect(screen, (255, 180, 0), (size[0]/2 - 100, size[1]/2 + 40, 200, 60), border_radius=6)

        # Button labels
        redo_label_1 = small_font.render("Redo", True, (0, 0, 0))
        screen.blit(redo_label_1, redo_label_1.get_rect(center=redo_button_1.center))

        redo_label_2 = small_font.render("Redo", True, (0, 0, 0))
        screen.blit(redo_label_2, redo_label_2.get_rect(center=redo_button_2.center))

        back_label = small_font.render("Level Select", True, (0, 0, 0))
        screen.blit(back_label, back_label.get_rect(center=back_button.center))

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
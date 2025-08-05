from utilities import lvls, pygame, run


pygame.init()
window = pygame.display.set_mode(flags=pygame.RESIZABLE)
window_size = window.get_size()
pygame.display.set_caption("RollRunner")


unlocked_levels = 1
while True:
    selected_level = lvls(window, unlocked_levels)
    success = run(selected_level)
    if success:
        unlocked_levels = max(unlocked_levels, selected_level + 1)

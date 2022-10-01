# screen resizing tut, dafluffypotato: https://www.youtube.com/watch?v=edJZOQwrMKw

import pygame, sys
from level import Level
from game_data import level_0, controller_map

# General setup
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
# tells pygame what events to check for
#setallowed
pygame.font.init()
clock = pygame.time.Clock()
game_speed = 60

# Screen Setup
# pygame.display.Info normally gets display dimensions. If there is no active display it takes the user's screen dimensions
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
# https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
# https://www.reddit.com/r/pygame/comments/r943bn/game_stuttering/
# vsync only works with scaled flag. Scaled flag will only work in combination with certain other flags.
# although resizeable flag is present, window can not be resized, only fullscreened with vsync still on
# vsync prevents screen tearing (multiple frames displayed at the same time creating a shuddering wave)
screen = pygame.display.set_mode((monitor_size[0], monitor_size[1]), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.SCALED, vsync=True)
screen_rect = screen.get_rect()  # used for camera scroll boundaries
pygame.display.set_caption('Toast Game')

# controller
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(f'joy {len(joysticks)}')
for joystick in joysticks:
    joystick.init()

def main_menu():
    game()


def game():
    click = False
    pause = False
    level = Level(level_0, screen, screen_rect, joysticks)

    running = True
    while running:

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()

        # Event Checks (input)
        click = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # debug keys
                if event.key == pygame.K_SLASH:
                    pass
                elif event.key == pygame.K_PERIOD:
                    pass
                elif event.key == pygame.K_p:
                    pause = not pause
                elif event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == controller_map['left_analog_press']:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.button == controller_map['options']:
                    pause = not pause

        # Update
        if not pause:
            screen.fill((98, 74, 41))
            level.run()

        print(clock.get_fps())
        pygame.display.flip()
        clock.tick(game_speed)


main_menu()


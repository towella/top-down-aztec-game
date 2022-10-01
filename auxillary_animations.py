import pygame
from support import import_folder

# TODO improve integration of auxanimation


class AuxAnimation(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.4
        self.frames = import_folder(path, 'list')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate_terminate(self):
        self.frame_index += self.animation_speed  # increments frame index by speed
        # if the animation is over, kill instance
        if self.frame_index >= len(self.frames):
            self.kill()
        # if animation is still running
        else:
            self.image = self.frames[int(self.frame_index)]

    def animate_loop(self):
        self.frame_index += self.animation_speed  # increments frame index by speed
        # if the animation is over, kill instance
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def apply_scroll(self, scroll_value):
        self.rect.x -= int(scroll_value[1])
        self.rect.y -= int(scroll_value[0])

    # updates animation, including camera movement and animates until the animation is done then kills
    def update(self, pos, scroll_value):
        self.animate_terminate()
        self.apply_scroll(scroll_value)


class DashTrail(AuxAnimation):
    def __init__(self, pos, direction):
        super().__init__(pos, '../graphics/animations/player/dash_trail')
        self.direction = direction

        # TODO make more efficient

        # rotates and positions the trail based on the player angle
        if direction == 'down':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], 90)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midbottom=pos)
        elif direction == 'up':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], -90)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midtop=pos)
        elif direction == 'right':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], 180)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(midright=pos)
        elif direction == 'downleft':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], 45)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(bottomleft=pos)
        elif direction == 'downright':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], 135)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(bottomright=pos)
        elif direction == 'upright':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], -135)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(topright=pos)
        elif direction == 'upleft':
            for frame in range(len(self.frames)):
                self.frames[frame] = pygame.transform.rotate(self.frames[frame], -45)
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect(topleft=pos)
        else:
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(midleft=pos)

    # TODO make more efficient
    # arbitrary numbers to center flame more nicely
    def center_to_player(self, pos):
        if self.direction == 'down':
            self.rect.midbottom = pos
        elif self.direction == 'up':
            self.rect.midtop = pos
        elif self.direction == 'right':
            self.rect.midright = (pos[0] - 20, pos[1])
        elif self.direction == 'downleft':
            self.rect.bottomleft = (pos[0] - 10, pos[1] + 10)
        elif self.direction == 'downright':
            self.rect.bottomright = (pos[0] + 10, pos[1] + 10)
        elif self.direction == 'upright':
            self.rect.topright = (pos[0] + 10, pos[1] - 10)
        elif self.direction == 'upleft':
            self.rect.topleft = (pos[0] - 10, pos[1] - 10)
        else:
            self.rect.midleft = (pos[0] + 20, pos[1])

    # updates dust animation, including shifting it on the x with the rest of the world
    def update(self, pos, scroll_value):
        self.animate_terminate()
        self.center_to_player(pos)

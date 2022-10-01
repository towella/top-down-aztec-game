import pygame
from game_data import tile_size, controller_map
from support import import_folder
from auxillary_animations import DashTrail


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, controllers):
        super().__init__()
        self.surface = surface
        self.controllers = controllers

        # -- animation and assets --
        self.import_character_assets()
        self.frame_index = 0
        self.status_facing = 'up'
        self.status_action = 'idle'
        self.animation_speed = 0.17
        self.image = self.animations['idle/down'][self.frame_index]

        # -- player setup --
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))  # used for movement and keeping track of images
        self.hitbox = self.hitboxes['up-down'].get_rect(topleft=self.rect.topleft)  # used for collisions

        # -- player movement --
        # collisions -- provides a buffer allowing late collision (must be higher than max velocity to prevent phasing)
        self.collision_tolerance = 20
        # walk
        self.direction = pygame.math.Vector2(0, 0)  # allows cleaner movement by storing both x and y direction

        # in one variable. x and y can also be accessed separately
        # speed_x and speed_y are required to be separate for proper camera movement, setting either value to 0 independantly
        self.speed_x = 4
        self.speed_y = 4

        # dash (time units are in frames (60fps), speed units are in multiples of player_speed)
        self.dash_length = 10
        self.dash_cooldown = 20
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dashing = False
        self.dash_key = False  # whether dash key is pressed or not (to prevent holding dash)
        self.dash_speed = 3.75
        self.diagonal_dash_speed = self.dash_speed * 0.7

        # -- aux animations --
        self.dash_trail = pygame.sprite.GroupSingle()

    # imports all character animations from folders
    def import_character_assets(self):
        animations_path = '../graphics/animations/player/'
        hitboxes_path = '../graphics/hitboxes/player/'
        self.hitboxes = {'up-down': None, 'left-right': None}
        self.animations = {'idle/down': [], 'idle/up': [], 'idle/right': [], 'idle/left': [],
                           'run/down': [], 'run/up': [], 'run/right': [], 'run/left': [],
                           'dash/down': [], 'dash/up': [], 'dash/right': [], 'dash/left': []}  # dictionary keys are the same name as folder
        # Only images in folders!

        # retrieve assets
        for animation in self.animations.keys():
            full_path = animations_path + animation  # extends directory pointer with desired animation folder
            self.animations[animation] = import_folder(full_path, 'list')
        for hitbox in self.hitboxes.keys():
            full_path = hitboxes_path + hitbox
            self.hitboxes[hitbox] = import_folder(full_path, 'surface')

    def change_hitbox(self):
        # left and right run and idle hitbox
        if 'right' in self.status_facing or 'left' in self.status_facing:
            # centers hitbox rather than being set at topleft
            self.hitbox = self.hitboxes['left-right'].get_rect(midtop=self.rect.midtop)
        # up and down run and idle hitbox
        elif 'up' in self.status_facing or 'down' in self.status_facing:
            self.hitbox = self.hitboxes['up-down'].get_rect(midtop=self.rect.midtop)

    def animate(self):
        facing = self.status_facing
        # sets facing to right or left for diagonals. (horizontal facing is prioritized over vertical for diagonals)
        if 'right' in facing:
            facing = 'right'
        elif 'left' in facing:
            facing = 'left'

        # gets needed animation
        anim_name = self.status_action + '/' + facing
        animation = self.animations[anim_name]

        # animation speed control
        if 'run' in anim_name and ('left' in anim_name or 'right' in anim_name):
            self.animation_speed = 0.2
        elif 'dash' in anim_name:
            self.animation_speed = 0.4
        else:
            self.animation_speed = 0.15

        # loop through animation at desired speed
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.change_hitbox()

    # player input and movement
    def get_input(self):
        keys = pygame.key.get_pressed()

        self.direction = pygame.Vector2(0, 0)
        # prevents movement during dash
        # TODO remove eventually
        if keys[pygame.K_x]:
            if self.speed_x == 4:
                self.speed_x = 15
                self.speed_y = 15
            else:
                self.speed_x = 4
                self.speed_y = 4
        if not self.dashing:
            # horizontal movement
            # self.controller.get_hat(0) returns tuple (x, y) for d-pad where 0, 0 is centered, -1 = left or down, 1 = right or up
            # the 0 refers to the dpad on the controller
            if keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.controller_input('right'):
                self.direction.x = 1
                self.status_action = 'run'
            if keys[pygame.K_LEFT] or keys[pygame.K_a] or self.controller_input('left'):
                self.direction.x = -1
                self.status_action = 'run'
            # vertical movement
            if keys[pygame.K_DOWN] or keys[pygame.K_s] or self.controller_input('down'):
                self.direction.y = 1
                self.status_action = 'run'
            if keys[pygame.K_UP] or keys[pygame.K_w] or self.controller_input('up'):
                self.direction.y = -1
                self.status_action = 'run'
        # TODO give back movement part way throught the dash using dash timer
        # allows one component of dash to be reset when dash key is not pressed, preventing holding dash
        if not keys[pygame.K_i] and not self.controller_input('dash'):
            self.dash_key = False
        # if dash key pressed and cool-down is over (enabling movement during cool-down) and not holding dash key, dash
        if (keys[pygame.K_i] or self.controller_input('dash')) and self.dash_cooldown_timer > self.dash_cooldown and not self.dash_key:
            self.dashing = True  # dashing is therefore only enabled after cool-down, making further checks redundant
            self.dash_key = True
            self.status_action = 'dash'
            self.frame_index = 0
            self.dash_trail.add(DashTrail((self.rect.centerx, self.rect.centery), self.status_facing))

        # diagonal velocity reduction (pythagoras means the diagonal movement is faster)
        # should be divided by root2 or 1.414 but this value feels nicer
        if self.direction.x != 0 and self.direction.y != 0:
            self.direction.x /= 1.3
            self.direction.y /= 1.3
        self.get_status()

    # checks controller inputs and returns true or false based on passed check
    def controller_input(self, input_check):
        # check if controllers are connected before getting controller input (done every frame preventing error if suddenly disconnected)
        if len(self.controllers) > 0:
            controller = self.controllers[0]
            if input_check == 'right':
                if controller.get_hat(0)[0] == 1 or (0.2 < controller.get_axis(controller_map['left_analog_x']) <= 1):
                    return True
            elif input_check == 'left':
                if controller.get_hat(0)[0] == -1 or (-0.2 > controller.get_axis(controller_map['left_analog_x']) >= -1):
                    return True
            elif input_check == 'up':
                if controller.get_hat(0)[1] == 1 or (-0.2 > controller.get_axis(controller_map['left_analog_y']) >= -1):
                    return True
            elif input_check == 'down':
                if controller.get_hat(0)[1] == -1 or (0.2 < controller.get_axis(controller_map['left_analog_y']) <= 1):
                    return True
            elif input_check == 'dash':
                if controller.get_button(controller_map['R2']) > 0.8 or controller.get_button(controller_map['triangle']) == 1:
                    return True
        return False

    # if the dash input has been given, increment the dash timer and see if the dash has reached it's full duration,
    # if it has, kill the dash and reset the dash cooldown
    def dash(self):
        # pythagoras
        if self.dashing:
            self.dash_timer += 1
            self.status_action = 'dash'
            # has to be greater than, dont change
            if self.dash_timer > self.dash_length:
                self.dashing = False
                self.dash_timer = 0
                self.status_action = 'idle'
                self.dash_cooldown_timer = 0
            else:
                # 4 axis
                if self.status_facing == 'up':
                    self.direction.y -= self.dash_speed
                elif self.status_facing == 'down':
                    self.direction.y += self.dash_speed
                elif self.status_facing == 'right':
                    self.direction.x += self.dash_speed
                elif self.status_facing == 'left':
                    self.direction.x -= self.dash_speed
                # diagonals
                elif self.status_facing == 'downright':
                    self.direction.x += self.diagonal_dash_speed
                    self.direction.y += self.diagonal_dash_speed
                elif self.status_facing == 'downleft':
                    self.direction.x -= self.diagonal_dash_speed
                    self.direction.y += self.diagonal_dash_speed
                elif self.status_facing == 'upright':
                    self.direction.x += self.diagonal_dash_speed
                    self.direction.y -= self.diagonal_dash_speed
                elif self.status_facing == 'upleft':
                    self.direction.x -= self.diagonal_dash_speed
                    self.direction.y -= self.diagonal_dash_speed

        else:
            self.dash_cooldown_timer += 1

    # gets player status based on a passed vector2 (either direction or a scroll vector to enable collisions)
    # vector2[0] = x, vector2[1] = y
    # vertical status takes priority over horizontal for animation purposes
    def get_status(self):
        if self.direction.x > 0 and self.direction.y > 0:
            self.status_facing = 'downright'
        elif self.direction.x < 0 and self.direction.y < 0:
            self.status_facing = 'upleft'
        elif self.direction.x > 0 and self.direction.y < 0:
            self.status_facing = 'upright'
        elif self.direction.x < 0 and self.direction.y > 0:
            self.status_facing = 'downleft'
        elif self.direction.y > 0:
            self.status_facing = 'down'
        elif self.direction.y < 0:
            self.status_facing = 'up'
        elif self.direction.x > 0:
            self.status_facing = 'right'
        elif self.direction.x < 0:
            self.status_facing = 'left'
        else:
            self.status_action = 'idle'

    # clearcode tut: https://www.youtube.com/watch?v=1_H7InPMjaY (main collision maths)
    # combined with dafluffypotato tut: https://www.youtube.com/watch?v=a_YTklVVNoQ (splitting the collisions to axis)
    def collision_x(self, tiles):
        for tile in tiles:
            if tile.hitbox.colliderect(self.hitbox):
                # abs ensures only the desired side registers collision
                # not having collisions dependant on status allows hitboxes to change size
                if abs(tile.hitbox.right - self.hitbox.left) < self.collision_tolerance: #and 'left' in self.status_facing:
                    self.hitbox.left = tile.hitbox.right
                elif abs(tile.hitbox.left - self.hitbox.right) < self.collision_tolerance: #and 'right' in self.status_facing:
                    self.hitbox.right = tile.hitbox.left
        # resyncs up rect to the hitbox
        self.rect.midtop = self.hitbox.midtop

    def collision_y(self, tiles):
        for tile in tiles:
            if tile.hitbox.colliderect(self.hitbox):
                # abs ensures only the desired side registers collision
                if abs(tile.hitbox.top - self.hitbox.bottom) < self.collision_tolerance: #and 'down' in self.status_facing:
                    self.hitbox.bottom = tile.hitbox.top
                elif abs(tile.hitbox.bottom - self.hitbox.top) < self.collision_tolerance: #and 'up' in self.status_facing:
                    self.hitbox.top = tile.hitbox.bottom
        # resyncs up rect to the hitbox
        self.rect.midtop = self.hitbox.midtop

    def apply_scroll(self, scroll_value):
        self.rect.x -= int(scroll_value[1])
        self.rect.y -= int(scroll_value[0])

    def update(self, tiles, scroll_value):
        # input and state handling
        self.get_input()
        self.dash()

        # animation
        self.animate()

        # x and y collisions are separated to make diagonal collisions easier and simpler to handle
        self.rect.x += int(self.direction.x * self.speed_x)
        # resyncs up hitbox to the rect
        self.hitbox.midtop = self.rect.midtop
        self.collision_x(tiles)
        # resyncs up hitbox to the rect
        self.rect.y += int(self.direction.y * self.speed_y)
        self.hitbox.midtop = self.rect.midtop
        self.collision_y(tiles)

        self.dash_trail.update((self.rect.centerx, self.rect.centery), scroll_value)

        # scroll shouldn't have collision applied, it is separate movement
        self.apply_scroll(scroll_value)

    # gets the layering of the sprites in the right order
    def draw(self):
        if self.status_facing == 'up':
            self.surface.blit(self.image, self.rect)
            self.dash_trail.draw(self.surface)
        else:
            self.dash_trail.draw(self.surface)
            self.surface.blit(self.image, self.rect)

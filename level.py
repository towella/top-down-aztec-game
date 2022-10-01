import pygame
from game_data import tile_size
from tiles import StaticTile
from player import Player
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, surface, display_rect, controllers):
        # level setup
        self.display_surface = surface  # main display surface
        self.display_rect = display_rect
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.controllers = controllers

        # takes in csvs into dictionary with same key (layer) names
        self.layer_data = {}
        for csv in level_data:
            self.layer_data[csv] = import_csv_layout(level_data[csv])
        # creates list of tile textures
        self.tile_textures = import_cut_graphics(f'../graphics/tiles/tilesets/tileset.png', 16)  # TODO fix directory and file selection when art is done

        # turns csv into coresponding tiles in a sprite group
        self.all_tiles = pygame.sprite.Group()  # contains all tiles for ease of scrolling

        # outside
        self.outside_shadows = self.create_tile_group(self.layer_data['outside_shadows'], 'static')
        self.outside_foreground = self.create_tile_group(self.layer_data['outside_foreground'], 'static')
        self.ceiling = self.create_tile_group(self.layer_data['ceiling'], 'static')
        self.outside_collideable = self.create_tile_group(self.layer_data['outside_collideable'], 'static')
        self.outside_background = self.create_tile_group(self.layer_data['outside_background'], 'static')
        self.outside_ground = self.create_tile_group(self.layer_data['outside_ground'], 'static')
        self.outside_NPC = self.create_tile_group(self.layer_data['outside_NPC'], 'static')

        # inside
        self.inside_shadows = self.create_tile_group(self.layer_data['inside_shadows'], 'static')
        self.inside_foreground = self.create_tile_group(self.layer_data['inside_foreground'], 'static')
        self.inside_collideable = self.create_tile_group(self.layer_data['inside_collideable'], 'static')
        self.inside_background = self.create_tile_group(self.layer_data['inside_background'], 'static')
        self.inside_ground = self.create_tile_group(self.layer_data['inside_ground'], 'static')

        # other
        self.create_tile_group(self.layer_data['player'], 'player')
        self.camera_boundaries_x = self.create_tile_group(self.layer_data['camera_boundaries_x'], 'static')
        self.camera_boundaries_y = self.create_tile_group(self.layer_data['camera_boundaries_y'], 'static')
        self.transitions = self.create_tile_group(self.layer_data['transitions'], 'static')
        print('tr', len(self.transitions))

        self.collideable = pygame.sprite.Group()  # contains all collideable tiles
        # loops through both groups (tile in either group)
        for tile in self.outside_collideable:
            self.collideable.add(tile)
        for tile in self.inside_collideable:
            self.collideable.add(tile)

        # camera setup
        # set camera to player imediately
        player = self.player.sprite
        self.screen_x_center = self.screen_width // 2
        self.screen_y_center = self.screen_height // 2
        # scroll is the player's center coordinates, offset to make the player in the center rather than at the origin
        # TODO prevent slight movement on start (caused by the world still scrolling as the display starts working)
        self.scroll_value = [player.rect.centery - self.screen_y_center, player.rect.centerx - self.screen_x_center]
        # update everything's position with the new scroll
        player.apply_scroll(self.scroll_value)
        self.all_tiles.update(self.scroll_value)

    # sets up tile sprite group based on level data
    '''def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):  # enumerate gives the index and information (!so cool!)
            for column_index, cell in enumerate(row):
                x = column_index * tile_size  # sets x coordinate
                y = row_index * tile_size  # sets y coordinate

                # checks for tile
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                # checks for player
                elif cell == 'P':
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)'''

    # creates all the neccessary types of tiles seperately and places them in individual layer groups
    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        # layers must have the same name as directories and file names

        for row_index, row in enumerate(layout):  # enumerate gives index and row list
            for column_index, val in enumerate(row):
                # if the tile isn't empty space
                if val != '-1':
                    x = column_index * tile_size
                    y = row_index * tile_size

                    # static
                    if type == 'static':
                        tile_surface = self.tile_textures[int(val)]  # the index of the surface is the same as the csv
                        # values as a result of the way the tilesheet is sliced and placed in the list
                        # essentially automatically coresponds number with tile type without copious if statements
                        sprite = StaticTile((x, y), tile_size, tile_surface)
                        sprite_group.add(sprite)
                        self.all_tiles.add(sprite)

                    if type == 'player':
                        if val == '2':
                            player_sprite = Player((x, y), self.display_surface, self.controllers)
                            self.player = pygame.sprite.GroupSingle(player_sprite)

                    '''# static
                    elif type == 'grass':
                        grass_tile_list = import_cut_graphics('../graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, (x, y), tile_surface)


                    # animated
                    elif type == 'coins':
                        if val == '0':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/gold')
                        elif val == '1':
                            sprite = Coin(tile_size, x, y, '../graphics/coins/silver')

                    # animated
                    elif type == 'fg palms':
                        if val == '0':
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_small',
                                          38)  # offset done here (different palm sizes)
                        elif val == '1':
                            sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_large',
                                          70)  # offset done here (different palm sizes)

                    # animated
                    elif type == 'bg palms':
                        sprite = Palm(tile_size, x, y, '../graphics/terrain/palm_bg',
                                      64)  # offset done here (different palm sizes)

                    # enemy
                    elif type == 'enemies':
                        sprite = Enemy(tile_size, x, y, '../graphics/enemy/run')

                    elif type == 'constraint':
                        sprite = Tile(tile_size, x, y)'''

        return sprite_group

    # scrolls the world when the player hits certain points on the screen
    # dynamic camera tut, dafluffypotato:  https://www.youtube.com/watch?v=5q7tmIlXROg
    def scroll(self):

        player = self.player.sprite
        buffer = 30  # changes scroll speed
        collision_tolerance = 60  # how far onto the screen a tile can be to be detected and prevent scrolling

        # scroll_value[0] = y, scroll_value[1] = x

        # scroll value cancels player movement with scrolling everything, including player (centerx - scroll_value)
        # subtracts screen width//2 to place player in the center of the screen rather than left edge

        # the division adds a fraction of the difference between the camera (scroll) and the player to the scroll,
        # making the camera follow with lag and also settle gently as the  fraction gets smaller the closer the camera
        # is to the player

        # self.scroll_value[1] += (player.rect.centerx - self.scroll_value[1] - screen_width//2)/20   for platformer
        # += was an issue causing odd motion (use for screen shake??)
        self.scroll_value[1] = (player.rect.centerx - self.scroll_value[1] - self.screen_x_center)/buffer
        self.scroll_value[0] = (player.rect.centery - self.scroll_value[0] - self.screen_y_center)/buffer

        # enables scroll camera boundaries
        screen_right = self.display_rect.right
        screen_left = 0
        screen_top = 0
        screen_bottom = self.display_rect.bottom  # may not appear to work as a result of the screen rect being set to fullscreen making screen bigger
        for tile in self.camera_boundaries_x:
            # neccessary to use a variable to be able to manipulate value
            tile_right = tile.rect.right
            tile_left = tile.rect.left
            # if the tile's right is on the right side within a certain area of the screen and we're scrolling left
            # (chained expression for efficiency)
            if collision_tolerance > tile.rect.right >= screen_left and self.scroll_value[1] < 0:
                # stop scroll
                self.scroll_value[1] = 0
                # while the tile's right is on screen
                while tile_right > screen_left:
                    # moving the camera to snap to tile grid by rounding the scroll value to a multiple of a tile
                    # (moving the camera until the tile is offscreen by exactly one pixel)
                    self.scroll_value[1] += 1
                    tile_right -= 1  # (positive scroll moves everything negatively) simulates the tile moving away
                    # without actually updating the tile pos, enables checking if the scroll is enough
                # after moving the camera we dont need to cycle through the rest of the tiles
                break
            elif (screen_right - collision_tolerance) < tile.rect.left <= screen_right and self.scroll_value[1] > 0:
                self.scroll_value[1] = 0
                while tile_left < screen_right:
                    self.scroll_value[1] -= 1
                    tile_left += 1
                break

        for tile in self.camera_boundaries_y:
            tile_bottom = tile.rect.bottom
            tile_top = tile.rect.top
            if collision_tolerance > tile.rect.bottom >= screen_top and self.scroll_value[0] < 0:
                self.scroll_value[0] = 0
                while tile_bottom > screen_top:
                    self.scroll_value[0] += 1
                    tile_bottom -= 1
                break
            elif (screen_bottom - collision_tolerance) < tile.rect.top <= screen_bottom and self.scroll_value[0] > 0:
                self.scroll_value[0] = 0
                while tile_top < screen_bottom:
                    self.scroll_value[0] -= 1
                    tile_top += 1
                break

        # non dynamic scroll system where player hits edges of set box on screen causing 2 dimensional scroll
        '''if player.rect.centerx < screen_width / 3 and direction_x < 0:
            self.scroll_value[1] = 4
            player.speed_x = 0
        elif player.rect.centerx > screen_width - (screen_width / 3) and direction_x > 0:
            self.scroll_value[1] = -4
            player.speed_x = 0
        else:
            self.scroll_value[1] = 0
            player.speed_x = 4

        if player.rect.centery < screen_height / 3 and direction_y < 0:
            self.scroll_value[0] = 4
            player.speed_y = 0
        elif player.rect.centery > screen_height - (screen_height / 3) and direction_y > 0:
            self.scroll_value[0] = -4
            player.speed_y = 0
        else:
            self.scroll_value[0] = 0
            player.speed_y = 4'''

    # draw tiles in tile group but only if in camera view
    def draw_tile_group(self, group):
        for tile in group:
            # if the tile is within the screen with a buffer of 100px every direction, render tile
            if tile.rect.right > -100 and tile.rect.left < self.screen_width + 100 and tile.rect.top > -100 and tile.rect.bottom < self.screen_height + 100:
                self.display_surface.blit(tile.image, tile.rect)

    # updates the level allowing tile scroll and displaying tiles to screen
    # order is equivalent of layers
    def run(self):
        render_ceiling = True

        # get current screen dimensions
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h

        # scroll -- must be first
        self.scroll()

        # Updates -- player needs to be before tiles for scroll to function properly
        self.player.update(self.collideable, self.scroll_value)
        self.all_tiles.update(self.scroll_value)
        for tile in self.ceiling:
            if self.player.sprite.rect.colliderect(tile):
                render_ceiling = False
                
        # Draw
        if render_ceiling:
            self.draw_tile_group(self.transitions)
            self.draw_tile_group(self.outside_ground)
            self.draw_tile_group(self.outside_background)
            # player.sprite references sprite.groupsingle's sprite rather than the group itself (calls different draw method in different class)
            self.player.sprite.draw()
            #self.player.sprite.draw_particles()
            self.draw_tile_group(self.outside_collideable)
            self.draw_tile_group(self.outside_NPC)
            self.draw_tile_group(self.ceiling)
            self.draw_tile_group(self.outside_shadows)
            self.draw_tile_group(self.outside_foreground)
        elif not render_ceiling:
            self.draw_tile_group(self.inside_ground)
            self.draw_tile_group(self.inside_background)
            # player.sprite references sprite.groupsingle's sprite rather than the group itself (calls different draw method in different class)
            self.player.sprite.draw()
            # self.player.sprite.draw_particles()
            self.draw_tile_group(self.inside_collideable)
            self.draw_tile_group(self.inside_shadows)
            self.draw_tile_group(self.inside_foreground)

# TODO fix player art
        # TODO  fix particles.py Parcticles class and organise the player file's particles handling
# TODO fix dash trail angle
# TODO make tile graphics
# TODO make tiles more efficent


# TODO make controller more responsive (analog) and possibly use scroll with an offset for second stick to look around?
# TODO animated tile class
# TODO implement delta time movement?? See how it goes
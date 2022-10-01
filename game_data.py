tile_size = 64  # 40 or 64 or 80 at 64 tilesize with 16 resolution, 4 real px per art px
#screen_width = 1280
#screen_height = 800

controller_map = {'square': 0, 'X': 1, 'circle': 2, 'triangle': 3, 'L1': 4, 'R1': 5, 'L2': 6, 'R2': 7, 'share': 8,
                  'options': 9, 'left_analog_press': 10, 'right_analog_press': 11, 'PS': 12, 'touchpad': 13,
                  'left_analog_x': 0,  'left_analog_y': 1}

level_0 = {
    'outside_shadows': '../csvs/level_test_outside_shadows.csv',
    'inside_shadows': '../csvs/level_test_inside_shadows.csv',
    'outside_foreground': '../csvs/level_test_outside_foreground.csv',
    'inside_foreground': '../csvs/level_test_inside_foreground.csv',
    'ceiling': '../csvs/level_test_ceiling.csv',
    'outside_collideable': '../csvs/level_test_outside_collideable.csv',
    'inside_collideable': '../csvs/level_test_inside_collideable.csv',
    'outside_NPC': '../csvs/level_test_outside_NPC.csv',
    'player': '../csvs/level_test_player.csv',
    'outside_background': '../csvs/level_test_outside_background.csv',
    'inside_background': '../csvs/level_test_inside_background.csv',
    'outside_ground': '../csvs/level_test_outside_ground.csv',
    'inside_ground': '../csvs/level_test_inside_ground.csv',
    'camera_boundaries_x': '../csvs/level_test_camera_boundaries_x.csv',
    'camera_boundaries_y': '../csvs/level_test_camera_boundaries_y.csv',
    'transitions': '../csvs/level_test_scene_transition_test.csv'}
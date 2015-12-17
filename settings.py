"""
Global variables
"""

# Name of the game
caption = "Planes"

# Display dimensions
display_width = 1300
display_height = 600

# Background
bg_speed = 7

# Basic colors
red = (210,0,0)
green = (0,117,0)
white = (255,255,255)
l_blue = (31, 181, 195)
d_blue = (7, 66, 79)

# Show/Hide mouse
mouse = True

# Plane properties
up_speed = 3
down_speed = 3
left_speed = 3
right_speed = 3

########################################################################################

# Ammo names and properties
ammo = {
    'bullet_1' : {
        'speed' : 10,
        'damage': 10,
        'lag'   : 10,
        'single': False,
        'x_off' : 7,          # Distance between bullet and png edge horizontally
        'y_off' : 17,         # Distance between bullet and png edge vertically
        'bullet_image' : "images/bullet.png",
        'bullet_icon_active'  : "images/primary_active.png",
        'bullet_icon_unactive'  : "images/primary_unactive.png",
        'bullet_icon_active_single' : "images/primary_active_single.png",
        'bullet_icon_unactive_single' : "images/primary_unactive_single.png",
    },
    'bullet_1_slow' : {
        'speed' : 10,
        'damage': 10,
        'lag'   : 15,
        'single': False,
        'x_off' : 7,          # Distance between bullet and png edge horizontally
        'y_off' : 17,         # Distance between bullet and png edge vertically
        'bullet_image' : "images/bullet.png",
        'bullet_icon_active'  : "images/primary_active.png",
        'bullet_icon_unactive'  : "images/primary_unactive.png",
        'bullet_icon_active_single' : "images/primary_active_single.png",
        'bullet_icon_unactive_single' : "images/primary_unactive_single.png",
    },
    'bullet_1_fast' : {
        'speed' : 10,
        'damage': 10,
        'lag'   : 7,
        'single': False,
        'x_off' : 7,          # Distance between bullet and png edge horizontally
        'y_off' : 17,         # Distance between bullet and png edge vertically
        'bullet_image' : "images/bullet.png",
        'bullet_icon_active'  : "images/primary_active.png",
        'bullet_icon_unactive'  : "images/primary_unactive.png",
        'bullet_icon_active_single' : "images/primary_active_single.png",
        'bullet_icon_unactive_single' : "images/primary_unactive_single.png",
    },
    'missile_1' : {
        'speed' : 10,
        'damage': 100,
        'lag'   : 50,
        'single': False,
        'x_off' : 7,
        'y_off' : 28,
        'bullet_image' : "images/missile_1.png",
        'bullet_icon_active'    : "images/secondary_active.png",
        'bullet_icon_unactive'  : "images/secondary_unactive.png"
    }
}


########################################################################################
# Enemy names and properties
enemy_info = {
    'blue_heli' : {
        'max_lives' : 100,
        'image' : "images/blue_heli.png",
        'wrecked_image' : "images/blue_heli_wrecked.png",
        'x_off': 60,
        'y_off': 70,
        'lives_x_off': 0,
        'lives_y_off': 130,
        'weapon_pos_x': 0,
        'weapon_pos_y': 0,
        'ammo'  : None,
        'shooting_resttime' : 0,
        'shooting_duration' : 0,
        'height' : 110,
        'value' : 50
    },
    'green_heli' : {
        'max_lives' : 180,
        'image' : "images/enemy2.png",
        'wrecked_image' : "images/enemy2_wrecked.png",
        'x_off': 60,
        'y_off': 121,
        'lives_x_off': 25,
        'lives_y_off': 160,
        'weapon_pos_x': -10,
        'weapon_pos_y': 22,
        'ammo'  : 'bullet_1_slow',
        'shooting_resttime' : 2,
        'shooting_duration' : 2,
        'height' : 66,
        'value' : 100
    },
    'green_heli_rockets' : {
        'max_lives' : 180,
        'image' : "images/enemy2.png",
        'wrecked_image' : "images/enemy2_wrecked.png",
        'x_off': 60,
        'y_off': 121,
        'lives_x_off': 25,
        'lives_y_off': 160,
        'weapon_pos_x': -10,
        'weapon_pos_y': 22,
        'ammo'  : 'missile_1',
        'shooting_resttime' : 2,
        'shooting_duration' : 2,
        'height' : 66,
        'value' : 150
    },
    'green_heli_enhanced' : {
        'max_lives' : 180,
        'image' : "images/enemy2.png",
        'wrecked_image' : "images/enemy2_wrecked.png",
        'x_off': 60,
        'y_off': 121,
        'lives_x_off': 25,
        'lives_y_off': 160,
        'weapon_pos_x': -10,
        'weapon_pos_y': 22,
        'ammo'  : 'bullet_1_fast',
        'shooting_resttime' : 2,
        'shooting_duration' : 2,
        'height' : 66,
        'value' : 170
    }
}

########################################################################################

# Bonus boxes
bonus_boxes_info = {
    'bullet_1_10' : {
        'type' : 'ammo',
        'reference' : 'bullet_1',
        'addition' : 10,
        'image' : "images/primary_active.png",
        'x_off': 60,
        'y_off': 70,
    }
}
########################################################################################
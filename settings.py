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

# Ammo names and properties
ammo = {
    'bullet_1' : {
        'speed' : 10,
        'damage': 20,
        'lag'   : 7,
        'single': False,
        'x_off' : 7,          # Distance between bullet and png edge horizontally
        'y_off' : 17,         # Distance between bullet and png edge vertically
        'bullet_image' : "images/bullet.png",
        'bullet_icon_active'  : "images/primary_active.png",
        'bullet_icon_unactive'  : "images/primary_unactive.png"
    },
    'missile_1' : {
        'speed' : 10,
        'damage': 50,
        'lag'   : 50,
        'single': False,
        'x_off' : 7,
        'y_off' : 28,
        'bullet_image' : "images/missile_1.png",
        'bullet_icon_active'    : "images/secondary_active.png",
        'bullet_icon_unactive'  : "images/secondary_unactive.png"
    }
}

# Enemy names and properties
enemy_info = {
    'blue_heli' : {
        'max_lives' : 100,
        'ammo'  : None,
        'image' : "images/blue_heli.png",
        'wrecked_image' : "images/blue_heli_wrecked.png",
        'x_off': 60,
        'y_off': 70,
        'height' : 110,
        'value' : 50
    }
}

# Bonus boxes
bonus_boxes_info = {
    'bullet_1_10' : {
        'type' : 'ammo',
        'addition' : 10,
        'image' : "images/bullet_1_10.png",
        'x_off': 60,
        'y_off': 70,
    }
}

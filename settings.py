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

# Show/Hide mouse
mouse = True

# Plane properties
up_speed = 3
down_speed = 3
left_speed = 3
right_speed = 3

# Ammo names and properties
ammo = \
    {
    'bullet_1' : {
        'speed' : 10,
        'damage': 10,
        'lag'   : 10,
        'x_off' : 7,          # Distance between bullet and png edge horizontally
        'y_off' : 17,         # Distance between bullet and png edge vertically
        'bullet_image' : "images/bullet.png"
    },
    'missile_1' : {
        'speed' : 20,
        'damage': 10,
        'lag'   : 0,
        'x_off' : 7,
        'y_off' : 17,
        'bullet_image' : "images/bullet.png"
    }}


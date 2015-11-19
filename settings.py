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

# Bullet_1 properties
bullet_1_speed = 10
bullet_1_lag = 10
bullet_1_damage = 10

# Missle_1 properties
missle_1_speed = 10
missle_1_lag = 0
missle_1_damage = 10

# Ammo names and properties
ammo = \
    {
    'bullet_1' : {
        'speed' : 10,
        'damage': 10,
        'lag'   : 10,
        'bullet_image' : "images/bullet.png"
    },
    'missile_1' : {
        'speed' : 20,
        'damage': 10,
        'lag'   : 0,
        'bullet_image' : "images/bullet.png"
    }}


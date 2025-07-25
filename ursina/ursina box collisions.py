from ursina import *
from ursina.shaders import lit_with_shadows_shader
import math
import time

app = Ursina(fullscreen=False, borderless=True, size=(1920,1080),
              development_mode=True, use_ingame_console=True)
window.editor_ui.enable()
total_runtime = 0
start_time = time.time()


player = Entity(model='cube', position=(0,0,0), texture='brick',
                 collider='box')

floor = Entity(model='plane', position=(0,-5,0), scale=10,
                texture='grass', collider='box')

wall_left = Entity(model='plane', position=(-5,0,0), scale=10,
                texture='brick', collider='box', rotation=(0,0,90))

wall_right = Entity(model='plane', position=(5,0,0), scale=10,
                texture='brick', collider='box', rotation=(0,0,-90))

ceiling = Entity(model='plane', position=(0,5,0), scale=10,
                texture='brick', collider='box', rotation= (0,0,180))

wall_back = Entity(model='plane', position=(0,0,5), scale=10,
                texture='brick', collider='box', rotation= (90,0,180), color= color.red)





def update():
    camera.look_at(player)
    speed = 5 * time.dt
    camera.rotation_z = 0

    if held_keys['w']:
        player.y *= speed
    if held_keys['s']:
        player.y /= speed
    if held_keys['a']:
        player.x -= speed
    if held_keys['d']:
        player.x += speed
    
    if held_keys['r']:
        camera.position = (0,0,-20)

    if player.intersects(floor).hit:
        player.y = floor.y + 0.5
    if player.intersects(wall_left).hit:
        player.x = wall_left.x + 0.5
    if player.intersects(wall_right).hit:
        player.x = wall_right.x - 0.5
    if player.intersects(ceiling).hit:
        player.y = ceiling.y - 0.5

EditorCamera()

app.run()
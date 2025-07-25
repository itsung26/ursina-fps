from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import time

app = Ursina(fullscreen=False, borderless=True, size=(1920,1080),
              development_mode=True, use_ingame_console=True)
window.editor_ui.enable()
total_runtime = 0
start_time = time.time()

# player entity- first person controller
player = FirstPersonController(
    model='cube',
    position=(0,10,0),
    rotation=(0,0,0),
    collider='box',
    shader=lit_with_shadows_shader
)


# sets the player jump height to higher
player.jump_height = 10
player.speed = 20
player.mouse_sensitivity = (100,100)

# Leave invisible the size changes based off of the resolution of the display used
player.cursor.scale = 0.000000000001

# game floor
floor = Entity(model='plane',
               position=(0,-5,0),
               scale=400,
               texture='grass',
               collider='box',
               Shader=lit_with_shadows_shader)

# enemy entity
enemy = Entity(model="vase-UV unwrapped.obj",
               position=(0,-5,20),
               scale=1,
               color=color.gray,
               #texture='rainbow',
               collider='box',
               #color=color.blue,
               Shader=lit_with_shadows_shader)

enemy.max_health = 100
enemy.health = 100

#healthbar entities- parent: enemy
enemy.health_bar_bg = Entity(
    parent=enemy,
    model='quad',
    color=color.gray,
    scale= 4 * (1.2, 0.1, 1),
    position=(0, 15, 0.1),
    rotation=(0,0,0)
)
enemy.health_bar = Entity(
    parent=enemy,
    model='quad',
    color=color.green,
    scale= 4 * (1, 0.08, 1),
    position=(0, 15, 0.1),
    rotation=(0,0,0)
)


def damage_enemy(amount):
    enemy.health = max(0, enemy.health - amount)
    enemy.health_bar.scale_x = enemy.health / enemy.max_health

def red_flash():
    enemy.color = color.red
    invoke(setattr, enemy, 'color', color.gray, delay=0.15)


debug_text_1 = Text("", position=(0,0))
debug_text_2 = Text("", position=(0,0.1))

mouse_position_text = Text("")

# variable definitions
can_print = True
cooldown_time = 0.1
last_shot_time = 0

# bullet list- contains all of the bullets currently rendered
bullets = []

def update():
    global can_print
    global cooldown_time
    global last_shot_time

    # updates the positions of the bullets.velocity every frame
    for bullet in bullets[:]:
        bullet.position += bullet.velocity


    if mouse.left:
        # if the cooldown has passed, create a bullet entity and append to bullets[]
        if time.time() - last_shot_time > cooldown_time:
            bullet = Entity(model='LP.obj',
                            position=player.position + player.forward * 5 + Vec3(0,2,0),
                            scale = 1,
                            texture='DefaultMaterial_Base_Color.png',
                            collider='box',
                            #color=color.red,
                            )
            
            # keeps the bullet pointing away from the camera
            bullet.look_at(bullet.position + camera.forward)
            bullet.velocity = camera.forward * 50 * time.dt
            bullets.append(bullet)
            last_shot_time = time.time()
        
        if can_print == True:
            # print statements used to check values of variables on click
            print(camera.forward)
            print(bullet.rotation)
            can_print = False

    if not mouse.left:
        can_print = True

    # if bullet hits something, hurt it
    for bullet in bullets:
        if bullet.intersects(enemy).hit:
            damage_enemy(2)
            red_flash()
            destroy(bullet)
            bullets.remove(bullet)
            break
    
    # if bullet hits floor, bounce it
    for bullet in bullets:
        if bullet.intersects(floor).hit:
            bullet.velocity.y *= -1
            bullet.position += bullet.velocity


# EditorCamera()

app.run()